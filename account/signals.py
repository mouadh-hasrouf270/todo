from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from notifications.models import Notification
from .models import MenuItem, MenuList,Restaurant

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    # Only run when updating an existing order
    if not created:
        if instance.status == 'confirmed':
            Notification.objects.create(
                user=instance.client.user,
                title="Order Confirmed",
                message=f"Your order #{instance.order_id} has been confirmed by {instance.restaurant.name}."
            )

        elif instance.status == 'ready':
            Notification.objects.create(
                user=instance.client.user,
                title="Order Ready",
                message=f"Your order #{instance.order_id} is ready for delivery from {instance.restaurant.name}."
            )

        elif instance.status == 'delivered':
            Notification.objects.create(
                user=instance.client.user,
                title="Order Delivered",
                message=f"Your order #{instance.order_id} has been delivered. Bon appétit!"
            )

@receiver(post_save, sender=MenuItem)
def add_item_to_restaurant_menu(sender, instance, created, **kwargs):
    if created:
        restaurant = instance.restaurant
        if restaurant and restaurant.menu_list:
            restaurant.menu_list.items.add(instance)


@receiver(post_save, sender=Restaurant)
def create_menu_list_for_restaurant(sender, instance, created, **kwargs):
    if created and instance.menu_list is None:
        menu_list = MenuList.objects.create(name=f"{instance.name} menu")
        instance.menu_list = menu_list
        instance.save()