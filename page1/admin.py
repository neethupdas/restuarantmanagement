from django.contrib import admin
from . models import Role,Person,Category,Menutbl,Subcategory,Table_Details,Cart,Order,TableReservation,Customization,Options,Reserved_Tables_Details,Selected_customization
# Register your models here.
admin.site.register(Role)
# Register your models here.
admin.site.register(Person)
admin.site.register(Category)
admin.site.register(Menutbl)
admin.site.register(Subcategory)
admin.site.register(Table_Details)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(TableReservation)
admin.site.register(Customization)
admin.site.register(Options)
admin.site.register(Reserved_Tables_Details)
admin.site.register(Selected_customization)







# {% for customization in customizations %}
#     {% if customization.menu_item_id == cartitem.item %}
#         {{ customization.description }}<br><br>
#         {% if customization.type == 0 %}
#             <!-- Checkbox -->
#             <table> 
#                 <tr>
#                     <th></th>
#                     <th></th>
#                 </tr>
                
#                 {% for option in options %}
#                     {% if option.customization == customization %}
#                         <form method="post" action="{% url 'c_apply_customization' cartitem.pk customization.pk %}">
#                             {% csrf_token %}
#                             <tr>
#                                 <center>
#                                     <td>
#                                         <input type="checkbox" name="option" value="{{ option.name }}" data-price="{{ option.price }}" onchange="updatePrice(this)" {% if option_is_selected(option.id) %} checked {% endif %}>
#                                         {{ option.name }}
#                                     </td>
#                                     <td align="left">
#                                         - {{ option.price }}
#                                     </td>
#                                 </center>
#                             </tr>
#                         </form>
#                     {% endif %}
#                 {% endfor %}
#                 <tr>
#                     <td>
#                         <button type="submit" name="apply_customization" >Apply</button>
#                     </td>
#                 </tr>
#             </table>
#         {% endif %}
#     {% endif %}
# {% endfor %}

# <script>
#     function option_is_selected(optionId) {
#         // Check if the option is selected based on its ID
#         {% for selected_customization in selected_customizations %}
#             if ({{ selected_customization.option_id }} == optionId) {
#                 return true;
#             }
#         {% endfor %}
#         return false;
#     }
# </script>
