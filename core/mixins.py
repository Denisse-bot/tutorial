from django.shortcuts import redirect

class SuperUsuarioMixin(object):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.usuario_administrador==True:
                return super().dispatch(request,*args,**kwargs)
        return redirect ('vista_usuario')