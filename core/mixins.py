from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect


class SuperUsuarioMixin(object):
    propiedad = False
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_staff == True:
            if request.user.is_nurse == True:
                return super().dispatch(request,*args,**kwargs)
            else:
                return HttpResponseRedirect(reverse_lazy('vista_funcionario'))
        return redirect('vista_usuario')
