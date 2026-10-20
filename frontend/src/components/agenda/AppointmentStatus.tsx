import { Chip } from "@mui/material";

import type { EstadoCita } from "../../api/tipos";

interface AppointmentStatusProps {
  status: EstadoCita;
}

// Los estados coinciden con los del backend (AppointmentStatus).
const colors: Record<EstadoCita, string> = {
  Confirmada: "#22C55E",
  Pendiente: "#F59E0B",
  Completada: "#3B82F6",
  Cancelada: "#EF4444",
};

export default function AppointmentStatus({
  status,
}: AppointmentStatusProps) {
  return (
    <Chip
      label={status}
      size="small"
      sx={{
        bgcolor: colors[status] ?? "#777",
        color: "#FFF",
        fontWeight: "bold",
        minWidth: 110,
      }}
    />
  );
}
