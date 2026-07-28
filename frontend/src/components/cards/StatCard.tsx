import { Card, CardContent, Typography, Box } from "@mui/material";
import type { ReactNode } from "react";

interface StatCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  color: string;
}

export default function StatCard({
  title,
  value,
  icon,
  color,
}: StatCardProps) {
  return (
    <Card
      sx={{
        borderRadius: 4,
        bgcolor: "#1E1E1E",
        color: "#FFFFFF",
        border: "1px solid rgba(255,255,255,.08)",
        transition: ".3s",

        "&:hover": {
          transform: "translateY(-5px)",
          boxShadow: "0px 12px 30px rgba(0,0,0,.35)",
        },
      }}
    >
      <CardContent>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Box>
            <Typography
              variant="body2"
              color="#BDBDBD"
            >
              {title}
            </Typography>

            <Typography
              variant="h4"
              fontWeight="bold"
              mt={1}
            >
              {value}
            </Typography>
          </Box>

          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: "50%",
              bgcolor: color,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              color: "#FFF",
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}