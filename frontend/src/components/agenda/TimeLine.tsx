import { Box } from "@mui/material";

import AppointmentCard from "./AppointmentCard";

export default function TimeLine() {
  return (
    <Box>
      <AppointmentCard
        hour="08:00"
        client="Carlos Gómez"
        barber="Juan Pérez"
        service="Corte Premium"
        status="Confirmada"
      />

      <AppointmentCard
        hour="09:00"
        client="Andrés López"
        barber="David Ramírez"
        service="Barba"
        status="Pendiente"
      />

      <AppointmentCard
        hour="10:30"
        client="Luis Martínez"
        barber="Juan Pérez"
        service="Corte + Barba"
        status="Finalizada"
      />

      <AppointmentCard
        hour="11:30"
        client="Santiago Ruiz"
        barber="Camilo Gómez"
        service="Corte Clásico"
        status="Confirmada"
      />
    </Box>
  );
}