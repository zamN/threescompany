from django.contrib import admin
# from UMagellan.models import Course, Route, Spot
from UMagellan.models import Course, Spot

class CourseAdmin(admin.ModelAdmin):
    pass

# class RouteAdmin(admin.ModelAdmin):
#     pass

class SpotAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Course, CourseAdmin)
# admin.site.register(Route, RouteAdmin)
admin.site.register(Spot, SpotAdmin)