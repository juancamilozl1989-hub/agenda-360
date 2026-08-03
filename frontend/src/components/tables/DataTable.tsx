import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import type { ReactNode } from "react";

interface Column {
  field: string;
  headerName: string;
  render?: (value: any, row: any) => ReactNode;
}

interface DataTableProps {
  columns: Column[];
  rows: any[];
  renderActions?: (row: any) => ReactNode;
}

export default function DataTable({
  columns,
  rows,
  renderActions,
}: DataTableProps) {
  return (
    <Paper
      sx={{
        borderRadius: 4,
        overflow: "hidden",
      }}
    >
      <Table>
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <TableCell key={column.field}>
                <strong>{column.headerName}</strong>
              </TableCell>
            ))}

            {renderActions && (
              <TableCell align="center">
                <strong>Acciones</strong>
              </TableCell>
            )}
          </TableRow>
        </TableHead>

        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id} hover>
              {columns.map((column) => (
                <TableCell key={column.field}>
                  {column.render
                    ? column.render(row[column.field], row)
                    : row[column.field]}
                </TableCell>
              ))}

              {renderActions && (
                <TableCell align="center">
                  {renderActions(row)}
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}