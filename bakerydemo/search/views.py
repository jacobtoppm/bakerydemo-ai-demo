from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page, get_page_models
from wagtail_vector_index.index.registry import registry

from bakerydemo.blog.models import BlogPage
from bakerydemo.breads.models import BreadPage
from bakerydemo.locations.models import LocationPage

from wagtail_vector_index.index.models import PageEmbeddableFieldsVectorIndex, VectorIndexedMixin

from wagtail_vector_index.index.exceptions import IndexedTypeFromDocumentError
from wagtail_vector_index.index.models import EmbeddableFieldsDocumentConverter

class SimilarPageDocumentConverter(EmbeddableFieldsDocumentConverter):
    def bulk_from_documents(
        self, documents
    ):
        docs = [doc for doc in documents]
        pages = {
            f"{p.pk}:{p.content_type_id}": p
            for p in self.base_model.objects.filter(
                pk__in={d.metadata["object_id"] for d in docs}
            )
        }
        for doc in docs:
            lookup_key = (
                f"{doc.metadata['object_id']}:{doc.metadata['content_type_id']}"
            )
            try:
                yield pages[lookup_key]
            except KeyError as e:
                raise IndexedTypeFromDocumentError(
                    "No object found for document"
                ) from e

@registry.register()
class AllPagesEmbeddableFieldsVectorIndex(PageEmbeddableFieldsVectorIndex):
    querysets = [
        model.objects.all() for model in get_page_models() if issubclass(model, VectorIndexedMixin)
    ]

    def get_converter_class(self):
        return SimilarPageDocumentConverter

    def get_converter(self):
        return self.get_converter_class()(Page)


def ai_query(request):
    index = AllPagesEmbeddableFieldsVectorIndex()
    query = request.GET.get("q", None)
    if query:
        result = index.query(query)

    return render(
        request,
        "search/question.html",
        {
            "query": query,
            "result": result if query else None
        },
    )



def search(request):
    # Search
    search_query = request.GET.get("q", None)
    if search_query:
        if "elasticsearch" in settings.WAGTAILSEARCH_BACKENDS["default"]["BACKEND"]:
            # In production, use ElasticSearch and a simplified search query, per
            # https://docs.wagtail.org/en/stable/topics/search/backends.html
            # like this:
            search_results = Page.objects.live().search(search_query)
        else:
            # If we aren't using ElasticSearch for the demo, fall back to native db search.
            # But native DB search can't search specific fields in our models on a `Page` query.
            # So for demo purposes ONLY, we hard-code in the model names we want to search.
            blog_results = BlogPage.objects.live().search(search_query)
            blog_page_ids = [p.page_ptr.id for p in blog_results]

            bread_results = BreadPage.objects.live().search(search_query)
            bread_page_ids = [p.page_ptr.id for p in bread_results]

            location_results = LocationPage.objects.live().search(search_query)
            location_result_ids = [p.page_ptr.id for p in location_results]

            page_ids = blog_page_ids + bread_page_ids + location_result_ids
            search_results = Page.objects.live().filter(id__in=page_ids)

        query = Query.get(search_query)

        # Record hit
        query.add_hit()

    else:
        search_results = Page.objects.none()

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search_results.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
