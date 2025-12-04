"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { getGuardians, deleteGuardian } from "@/services/guardianService";
import type { Guardian } from "@/types/student";
import { Search, Plus, Eye, Pencil, Trash2, Loader2, Users } from "lucide-react";
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog";

export default function GuardiansPage() {
    const router = useRouter();
    const [guardians, setGuardians] = useState<Guardian[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [guardianToDelete, setGuardianToDelete] = useState<Guardian | null>(null);

    useEffect(() => {
        loadGuardians();
    }, []);

    const loadGuardians = async () => {
        try {
            setLoading(true);
            const data = await getGuardians();
            setGuardians(data);
        } catch (error: any) {
            toast.error(error.message || "Failed to load guardians");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!guardianToDelete) return;

        try {
            await deleteGuardian(guardianToDelete.id);
            toast.success("Guardian deleted successfully");
            loadGuardians();
        } catch (error: any) {
            toast.error(error.message || "Failed to delete guardian");
        } finally {
            setDeleteDialogOpen(false);
            setGuardianToDelete(null);
        }
    };

    const filteredGuardians = guardians.filter((guardian) => {
        const matchesSearch =
            searchQuery === "" ||
            guardian.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            guardian.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            guardian.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
            guardian.phone_number.includes(searchQuery);

        return matchesSearch;
    });

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-2xl font-bold tracking-tight">Guardians</h3>
                    <p className="text-sm text-muted-foreground">
                        Manage parent and guardian information
                    </p>
                </div>
                <Link href="/guardians/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Guardian
                    </Button>
                </Link>
            </div>

            {/* Search */}
            <Card>
                <CardHeader>
                    <CardTitle>Search</CardTitle>
                    <CardDescription>Search guardians by name, email, or phone</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="relative">
                        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search by name, email, phone..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="pl-9"
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Guardians Table */}
            <Card>
                <CardContent className="p-0">
                    {loading ? (
                        <div className="flex items-center justify-center p-12">
                            <Loader2 className="h-8 w-8 animate-spin text-primary" />
                        </div>
                    ) : filteredGuardians.length === 0 ? (
                        <div className="flex flex-col items-center justify-center p-12 text-center">
                            <Users className="h-12 w-12 text-muted-foreground mb-4" />
                            <h3 className="text-lg font-semibold">No guardians found</h3>
                            <p className="text-sm text-muted-foreground mb-4">
                                {searchQuery
                                    ? "Try adjusting your search"
                                    : "Get started by adding a guardian"}
                            </p>
                            {!searchQuery && (
                                <Link href="/guardians/new">
                                    <Button>
                                        <Plus className="mr-2 h-4 w-4" />
                                        Add Guardian
                                    </Button>
                                </Link>
                            )}
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Relationship</TableHead>
                                    <TableHead>Email</TableHead>
                                    <TableHead>Phone</TableHead>
                                    <TableHead>Students</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredGuardians.map((guardian) => (
                                    <TableRow key={guardian.id}>
                                        <TableCell className="font-medium">
                                            {guardian.first_name} {guardian.last_name}
                                        </TableCell>
                                        <TableCell>{guardian.relationship}</TableCell>
                                        <TableCell>{guardian.email}</TableCell>
                                        <TableCell>{guardian.phone_number}</TableCell>
                                        <TableCell>{guardian.student.length}</TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => router.push(`/guardians/${guardian.id}`)}
                                                >
                                                    <Eye className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => router.push(`/guardians/${guardian.id}/edit`)}
                                                >
                                                    <Pencil className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => {
                                                        setGuardianToDelete(guardian);
                                                        setDeleteDialogOpen(true);
                                                    }}
                                                >
                                                    <Trash2 className="h-4 w-4 text-destructive" />
                                                </Button>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>

            {/* Delete Confirmation Dialog */}
            <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                            This will delete the guardian record for{" "}
                            <strong>
                                {guardianToDelete?.first_name} {guardianToDelete?.last_name}
                            </strong>
                            . This action cannot be undone.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction
                            onClick={handleDelete}
                            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                        >
                            Delete
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </div>
    );
}
