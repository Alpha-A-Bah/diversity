from django.shortcuts import render
from .models import Module, Diversity
from .forms import DiversityForm, ModuleForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from studentaccount.mixins import AdmissionsTeamRequiredMixin
from django.urls import reverse, reverse_lazy


class DashboardView(LoginRequiredMixin, generic.ListView):
    model = Module
    template_name = 'index.html'
    context_object_name = 'modules'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the 'diversityFilter' query parameter
        query = self.request.GET.get('diversityFilter')
        if query:
            # Filter diversity instances based on the query
            diversities = Diversity.objects.filter(ethnic_group=query)
            
            # Create a list to store module name and student count information
            diversity_info = []

            for diversity in diversities:
                module_name = diversity.module.name
                student_count = diversity.student_count
                diversity_info.append({'module_name': module_name, 'student_count': student_count})

            # Pass the diversity information to the context
            context['diversity_info'] = diversity_info
            context['query'] =query
        # Retrieve the list of diversities
        
        diversities = Diversity.objects.values_list('ethnic_group', flat=True).distinct()
        context['diversities'] = diversities
        return context


class DiversityView(LoginRequiredMixin, generic.ListView):
    model = Diversity
    context_object_name = 'diversity'
    template_name = 'diversity.html'


class CreateDiversityView(AdmissionsTeamRequiredMixin, generic.CreateView):
    model = Diversity
    fields = ['module', 'ethnic_group', 'student_count']
    template_name = 'create_diversity.html'

    def get_success_url(self):
        return reverse('diversity') 


class UpdateDiversityView(AdmissionsTeamRequiredMixin, generic.View):
    template_name = 'edit-diversity.html'

    def get(self, request, diversity_id):
        diversity = Diversity.objects.get(pk=diversity_id)
        form = DiversityForm(instance=diversity)
        context = {'form': form, 'diversity': diversity}
        return render(request, self.template_name, context)

    def post(self, request, diversity_id):
        diversity = Diversity.objects.get(pk=diversity_id)
        form = DiversityForm(request.POST, instance=diversity)
        
        if form.is_valid():
            form.save()
            return redirect('diversity') 
        
        context = {'form': form, 'diversity': diversity}
        return render(request, self.template_name, context)
    

class DeleteDiversityView(AdmissionsTeamRequiredMixin, generic.DeleteView):
    model = Diversity
    template_name = 'delete_diversity.html' 
    success_url = reverse_lazy('diversity') 
    pk_url_kwarg = 'diversity_id'


class ModuleListView(AdmissionsTeamRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        modules = Module.objects.all()
        context = {
            'modules':modules
        }
        return render(request, 'module_list.html', context=context)
    

class ModuleCreateView(AdmissionsTeamRequiredMixin, generic.CreateView):
    model = Module
    fields = ['name', 'description']  
    template_name = 'module_form.html' 
    success_url = reverse_lazy('module_list')


class ModuleUpdateView(AdmissionsTeamRequiredMixin, generic.View):
    template_name = 'module_form.html'  

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        form = ModuleForm(instance=module)  
        context = {'module': module, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        form = ModuleForm(request.POST, instance=module) 
        if form.is_valid():
            form.save()
            return redirect('module_list') 
        context = {'module': module, 'form': form}
        return render(request, self.template_name, context)


class DeleteModuleView(AdmissionsTeamRequiredMixin, generic.DeleteView):
    model = Module
    template_name = 'delete_diversity.html' 
    success_url = reverse_lazy('module_list') 
    pk_url_kwarg = 'module_id'




