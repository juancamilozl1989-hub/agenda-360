import {
  Avatar,
  Box,
  Divider,
  Paper,
  Typography,
} from "@mui/material";

const appointments = [
  {
    client: "Carlos Gómez",
    service: "Corte Clásico",
    time: "09:00 AM",
  },
  {
    client: "Andrés Pérez",
    service: "Barba Premium",
    time: "10:00 AM",
  },
  {
    client: "Felipe Ramírez",
    service: "Corte + Barba",
    time: "11:30 AM",
  },
  {
    client: "Juan Torres",
    service: "Perfilado",
    time: "02:00 PM",
  },
];

export default function RecentAppointments() {
  return (
    <Paper
      sx={{
        mt: 5,
        p: 4,
        borderRadius: 4,
        bgcolor: "#1E1E1E",
      }}
    >
      <Typography
        variant="h6"
        fontWeight="bold"
        mb={3}
      >
        Próximas citas de hoy
      </Typography>

      {appointments.map((appointment, index) => (
        <Box key={index}>
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
                {appointment.client.charAt(0)}
              </Avatar>

              <Box>
                <Typography fontWeight="bold">
                  {appointment.client}
                </Typography>

                <Typography
                  variant="body2"
                  color="gray"
                >
                  {appointment.service}
                </Typography>
              </Box>
            </Box>

            <Typography
              fontWeight="bold"
              color="#D4AF37"
            >
              {appointment.time}
            </Typography>
          </Box>

          {index < appointments.length - 1 && (
            <Divider />
          )}
        </Box>
      ))}
    </Paper>
  );
}