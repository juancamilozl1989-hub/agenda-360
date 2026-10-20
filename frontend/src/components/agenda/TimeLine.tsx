import { Box, Typography } from "@mui/material";

import AppointmentCard from "./AppointmentCard";
import type { Cita } from "../../api/tipos";

interface TimeLineProps {
  citas: Cita[];
  // Si es true se muestra también la fecha (vistas de semana y mes)
  mostrarFecha?: boolean;
  onEdit: (cita: Cita) => void;
  onDelete: (cita: Cita) => void;
}

export default function TimeLine({
  citas,
  mostrarFecha = false,
  onEdit,
  onDelete,
}: TimeLineProps) {
  if (citas.length === 0) {
    return (
      <Typography color="text.secondary" textAlign="center" py={4}>
        No hay citas registradas para este periodo.
      </Typography>
    );
  }

  return (
    <Box>
      {citas.map((cita) => (
        <AppointmentCard
          key={cita.id}
          hour={cita.hora.slice(0, 5)}
          date={mostrarFecha ? cita.fecha : undefined}
          client={cita.client.nombre}
          barber={cita.barber.nombre}
          service={cita.service.nombre}
          status={cita.estado}
          onEdit={() => onEdit(cita)}
          onDelete={() => onDelete(cita)}
        />
      ))}
    </Box>
  );
}
