import { Chip } from "@mui/material";

interface AppointmentStatusProps {
  status: "Confirmada" | "Pendiente" | "Finalizada";
}

export default function AppointmentStatus({
  status,
}: AppointmentStatusProps) {
  const colors = {
    Confirmada: "#22C55E",
    Pendiente: "#F59E0B",
    Finalizada: "#3B82F6",
  };

  return (
    <Chip
      label={status}
      size="small"
      sx={{
        bgcolor: colors[status],
        color: "#FFF",
        fontWeight: "bold",
        minWidth: 110,
      }}
    />
  );
}