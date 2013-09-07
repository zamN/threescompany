from django.contrib import admin
from UMagellan.models import Class, Route, POI

class ClassAdmin(admin.ModelAdmin):
    pass

class RouteAdmin(admin.ModelAdmin):
    pass

class POIAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Class, ClassAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(POI, POIAdmin)