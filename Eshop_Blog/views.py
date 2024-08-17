from django.views.generic import ListView, DetailView

from .models import Blog


# Create your views here.


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = 'Eshop_Blog/blog.html'
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.filter(is_active=True, is_delete=False).order_by('-id').all()


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'Eshop_Blog/blog-single.html'
