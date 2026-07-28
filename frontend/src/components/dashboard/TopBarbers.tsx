import {
  Avatar,
  Box,
  Paper,
  Typography,
} from "@mui/material";

const barbers = [
  {
    name: "Juan",
    appointments: 18,
  },
  {
    name: "Pedro",
    appointments: 15,
  },
  {
    name: "Luis",
    appointments: 12,
  },
];

export default function TopBarbers() {
  return (
    <Paper
      sx={{
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
        Barberos destacados
      </Typography>

      {barbers.map((barber) => (
        <Box
          key={barber.name}
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            mb: 3,
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
              }}
            >
              {barber.name.charAt(0)}
            </Avatar>

            <Typography>
              {barber.name}
            </Typography>
          </Box>

          <Typography
            color="#D4AF37"
            fontWeight="bold"
          >
            {barber.appointments} citas
          </Typography>
        </Box>
      ))}
    </Paper>
  );
}