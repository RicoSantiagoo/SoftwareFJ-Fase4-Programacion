   """
Módulo 4 - Modelo Reserva
Autor: Castaño - Compañero 3
Proyecto: SoftwareFJ - Fase 4
"""

from datetime import datetime

class Reserva:
    """
    Clase que representa una reserva de un cliente.
    """

    def __init__(self, id_reserva, cliente, servicio, fecha, hora, estado="pendiente"):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
        self.fecha_creacion = datetime.now()

    def confirmar(self):
        """Confirma la reserva."""
        self.estado = "confirmada"
        return f"Reserva {self.id_reserva} confirmada."

    def cancelar(self):
        """Cancela la reserva."""
        self.estado = "cancelada"
        return f"Reserva {self.id_reserva} cancelada."

    def cambiar_fecha(self, nueva_fecha, nueva_hora):
        """Cambia la fecha y hora de la reserva."""
        if self.estado == "cancelada":
            return "No se puede cambiar una reserva cancelada."
        self.fecha = nueva_fecha
        self.hora = nueva_hora
        return f"Reserva {self.id_reserva} reprogramada para {nueva_fecha} a las {nueva_hora}."

    def mostrar_info(self):
        """Muestra la información de la reserva."""
        return (
            f"ID: {self.id_reserva} | "
            f"Cliente: {self.cliente} | "
            f"Servicio: {self.servicio} | "
            f"Fecha: {self.fecha} {self.hora} | "
            f"Estado: {self.estado}"
        )

    def __str__(self):
        return self.mostrar_info()