"use client";

import { Search } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const searchResults = [
    { id: 1, name: "John Doe", type: "Student", id_number: "STU001", email: "john@example.com" },
    { id: 2, name: "Jane Smith", type: "Faculty", id_number: "FAC001", email: "jane@example.com" },
];

export default function SearchPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Search className="h-8 w-8 text-primary" />
                Search
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Search Database</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-2">
                        <Input placeholder="Search students, faculty, courses..." className="flex-1" />
                        <Button>
                            <Search className="mr-2 h-4 w-4" />
                            Search
                        </Button>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Search Results</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>ID</TableHead>
                                <TableHead>Email</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {searchResults.map((result) => (
                                <TableRow key={result.id}>
                                    <TableCell className="font-semibold">{result.name}</TableCell>
                                    <TableCell>{result.type}</TableCell>
                                    <TableCell className="font-mono text-sm">{result.id_number}</TableCell>
                                    <TableCell>{result.email}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
