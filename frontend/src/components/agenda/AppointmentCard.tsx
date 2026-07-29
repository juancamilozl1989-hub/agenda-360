import {
  Avatar,
  Box,
  Paper,
  Typography,
} from "@mui/material";

import AppointmentStatus from "./AppointmentStatus";

interface AppointmentCardProps {
  hour: string;
  client: string;
  barber: string;
  service: string;
  status: "Confirmada" | "Pendiente" | "Finalizada";
}

export default function AppointmentCard({
  hour,
  client,
  barber,
  service,
  status,
}: AppointmentCardProps) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2.5,
        mb: 2,
        borderRadius: 4,
        bgcolor: "#232323",
        border: "1px solid rgba(255,255,255,.08)",
        transition: ".3s",

        "&:hover": {
          transform: "translateY(-2px)",
          borderColor: "#D4AF37",
          boxShadow: "0 10px 25px rgba(0,0,0,.35)",
        },
      }}
    >
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
      >
        {/* Hora */}
        <Typography
          sx={{
            color: "#D4AF37",
            fontWeight: "bold",
            width: 80,
          }}
        >
          {hour}
        </Typography>

        {/* Información */}
        <Box
          display="flex"
          alignItems="center"
          flex={1}
          gap={2}
        >
          <Avatar
            sx={{
              bgcolor: "#2E2E2E",
              color: "#D4AF37",
            }}
          >
            {client.charAt(0)}
          </Avatar>

          <Box>
            <Typography
              fontWeight="bold"
              color="#FFF"
            >
              {client}
            </Typography>

            <Typography
              variant="body2"
              color="#AAA"
            >
              {service}
            </Typography>

            <Typography
              variant="caption"
              color="#888"
            >
              Barbero: {barber}
            </Typography>
          </Box>
        </Box>

        {/* Estado */}
        <AppointmentStatus status={status} />
      </Box>
    </Paper>
  );
}