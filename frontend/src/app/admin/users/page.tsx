"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
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
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { getUsers, deleteUser, activateUser, deactivateUser, resetUserPassword, User } from "@/services/userService";
import { getGroups, Group } from "@/services/groupService";
import { Search, Plus, Eye, Pencil, Trash2, Loader2, UserX, UserCheck, Key } from "lucide-react";
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
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

export default function UsersPage() {
    const router = useRouter();
    const [users, setUsers] = useState<User[]>([]);
    const [groups, setGroups] = useState<Group[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [filterActive, setFilterActive] = useState<string>("all");
    const [filterStaff, setFilterStaff] = useState<string>("all");
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [resetPasswordDialogOpen, setResetPasswordDialogOpen] = useState(false);
    const [selectedUser, setSelectedUser] = useState<User | null>(null);
    const [newPassword, setNewPassword] = useState("");

    useEffect(() => {
        fetchUsers();
        fetchGroups();
    }, []);

    const fetchUsers = async () => {
        try {
            setLoading(true);
            const data = await getUsers();
            setUsers(data);
        } catch (error) {
            toast.error("Failed to load users");
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const fetchGroups = async () => {
        try {
            const data = await getGroups();
            setGroups(data);
        } catch (error) {
            console.error(error);
        }
    };

    const handleSearch = async () => {
        try {
            setLoading(true);
            const filters: any = {};
            
            if (searchTerm) filters.search = searchTerm;
            if (filterActive !== "all") filters.is_active = filterActive === "active";
            if (filterStaff !== "all") filters.is_staff = filterStaff === "staff";
            
            const data = await getUsers(filters);
            setUsers(data);
        } catch (error) {
            toast.error("Failed to search users");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!selectedUser) return;

        try {
            await deleteUser(selectedUser.id);
            toast.success("User deleted successfully");
            setDeleteDialogOpen(false);
            fetchUsers();
        } catch (error) {
            toast.error("Failed to delete user");
        }
    };

    const handleActivateToggle = async (user: User) => {
        try {
            if (user.is_active) {
                await deactivateUser(user.id);
                toast.success("User deactivated successfully");
            } else {
                await activateUser(user.id);
                toast.success("User activated successfully");
            }
            fetchUsers();
        } catch (error) {
            toast.error(`Failed to ${user.is_active ? 'deactivate' : 'activate'} user`);
        }
    };

    const handleResetPassword = async () => {
        if (!selectedUser || !newPassword) {
            toast.error("Password is required");
            return;
        }

        try {
            await resetUserPassword(selectedUser.id, newPassword);
            toast.success("Password reset successfully");
            setResetPasswordDialogOpen(false);
            setNewPassword("");
        } catch (error) {
            toast.error("Failed to reset password");
        }
    };

    const getGroupNames = (groupIds: number[] | string[]) => {
        if (!groupIds || groupIds.length === 0) return "None";
        return groupIds
            .map(id => groups.find(g => g.id === Number(id))?.name || id)
            .join(", ");
    };

    const filteredUsers = users;

    return (
        <div className="container mx-auto py-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">User Management</h1>
                    <p className="text-muted-foreground">Manage system users and their permissions</p>
                </div>
                <Button onClick={() => router.push("/admin/users/create")}>
                    <Plus className="mr-2 h-4 w-4" /> Add User
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Search & Filter</CardTitle>
                    <CardDescription>Find users by username, email, or name</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-4">
                        <div className="flex-1">
                            <Input
                                placeholder="Search users..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                            />
                        </div>
                        <Select value={filterActive} onValueChange={setFilterActive}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Users</SelectItem>
                                <SelectItem value="active">Active Only</SelectItem>
                                <SelectItem value="inactive">Inactive Only</SelectItem>
                            </SelectContent>
                        </Select>
                        <Select value={filterStaff} onValueChange={setFilterStaff}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Staff Status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Types</SelectItem>
                                <SelectItem value="staff">Staff Only</SelectItem>
                                <SelectItem value="regular">Regular Only</SelectItem>
                            </SelectContent>
                        </Select>
                        <Button onClick={handleSearch}>
                            <Search className="mr-2 h-4 w-4" /> Search
                        </Button>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Users ({users.length})</CardTitle>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="flex justify-center p-8">
                            <Loader2 className="h-8 w-8 animate-spin" />
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Username</TableHead>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Email</TableHead>
                                    <TableHead>Groups</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Role</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredUsers.map((user) => (
                                    <TableRow key={user.id}>
                                        <TableCell className="font-medium">{user.username}</TableCell>
                                        <TableCell>{user.first_name} {user.last_name}</TableCell>
                                        <TableCell>{user.email}</TableCell>
                                        <TableCell>
                                            <span className="text-sm text-muted-foreground">
                                                {getGroupNames(user.groups)}
                                            </span>
                                        </TableCell>
                                        <TableCell>
                                            {user.is_active ? (
                                                <Badge variant="default">Active</Badge>
                                            ) : (
                                                <Badge variant="secondary">Inactive</Badge>
                                            )}
                                        </TableCell>
                                        <TableCell>
                                            {user.is_superuser ? (
                                                <Badge variant="destructive">Superuser</Badge>
                                            ) : user.is_staff ? (
                                                <Badge variant="outline">Staff</Badge>
                                            ) : (
                                                <Badge variant="secondary">User</Badge>
                                            )}
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => router.push(`/admin/users/${user.id}`)}
                                                >
                                                    <Eye className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => router.push(`/admin/users/${user.id}/edit`)}
                                                >
                                                    <Pencil className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => handleActivateToggle(user)}
                                                >
                                                    {user.is_active ? (
                                                        <UserX className="h-4 w-4" />
                                                    ) : (
                                                        <UserCheck className="h-4 w-4" />
                                                    )}
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => {
                                                        setSelectedUser(user);
                                                        setResetPasswordDialogOpen(true);
                                                    }}
                                                >
                                                    <Key className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => {
                                                        setSelectedUser(user);
                                                        setDeleteDialogOpen(true);
                                                    }}
                                                >
                                                    <Trash2 className="h-4 w-4" />
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

            <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                            This will permanently delete the user {selectedUser?.username}. This action cannot be undone.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>

            <Dialog open={resetPasswordDialogOpen} onOpenChange={setResetPasswordDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Reset Password</DialogTitle>
                        <DialogDescription>
                            Reset password for user: {selectedUser?.username}
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="new-password">New Password</Label>
                            <Input
                                id="new-password"
                                type="password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                placeholder="Enter new password"
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setResetPasswordDialogOpen(false)}>
                            Cancel
                        </Button>
                        <Button onClick={handleResetPassword}>Reset Password</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
