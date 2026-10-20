import {
  Avatar,
  Box,
  Divider,
  Paper,
  Typography,
} from "@mui/material";

import type { Cita } from "../../api/tipos";

interface RecentAppointmentsProps {
  citas: Cita[];
}

export default function RecentAppointments({
  citas,
}: RecentAppointmentsProps) {
  return (
    <Paper
      sx={{
        p: 4,
        borderRadius: 4,
        bgcolor: "#1E1E1E",
      }}
    >
      <Typography variant="h6" fontWeight="bold" mb={3}>
        Próximas citas de hoy
      </Typography>

      {citas.length === 0 && (
        <Typography color="text.secondary">
          No hay citas pendientes para hoy.
        </Typography>
      )}

      {citas.map((cita, index) => (
        <Box key={cita.id}>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              py: 2,
            }}
          >
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 2,
              }}
            >
              <Avatar
                sx={{
                  bgcolor: "#D4AF37",
                  color: "#121212",
                  fontWeight: "bold",
                }}
              >
                {cita.client.nombre.charAt(0)}
              </Avatar>

              <Box>
                <Typography fontWeight="bold">
                  {cita.client.nombre}
                </Typography>

                <Typography variant="body2" color="gray">
                  {cita.service.nombre}
                </Typography>
              </Box>
            </Box>

            <Typography fontWeight="bold" color="#D4AF37">
              {cita.hora.slice(0, 5)}
            </Typography>
          </Box>

          {index < citas.length - 1 && <Divider />}
        </Box>
      ))}
    </Paper>
  );
}
