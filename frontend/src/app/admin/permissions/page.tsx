"use client";

import { useState, useEffect } from "react";
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
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { getPermissions, getContentTypes, Permission, ContentType } from "@/services/permissionService";
import { Search, Loader2, Shield } from "lucide-react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

export default function PermissionsPage() {
    const [permissions, setPermissions] = useState<Permission[]>([]);
    const [contentTypes, setContentTypes] = useState<ContentType[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [filterContentType, setFilterContentType] = useState<string>("all");

    useEffect(() => {
        fetchPermissions();
        fetchContentTypes();
    }, []);

    const fetchPermissions = async () => {
        try {
            setLoading(true);
            const data = await getPermissions();
            setPermissions(data);
        } catch (error) {
            toast.error("Failed to load permissions");
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const fetchContentTypes = async () => {
        try {
            const data = await getContentTypes();
            setContentTypes(data);
        } catch (error) {
            console.error(error);
        }
    };

    const handleSearch = async () => {
        try {
            setLoading(true);
            const filters: any = {};
            
            if (searchTerm) filters.search = searchTerm;
            if (filterContentType !== "all") filters.content_type = filterContentType;
            
            const data = await getPermissions(filters);
            setPermissions(data);
        } catch (error) {
            toast.error("Failed to search permissions");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto py-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">Permission Management</h1>
                    <p className="text-muted-foreground">View all system permissions</p>
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Search & Filter</CardTitle>
                    <CardDescription>Find permissions by name or content type</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-4">
                        <div className="flex-1">
                            <Input
                                placeholder="Search permissions..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                            />
                        </div>
                        <Select value={filterContentType} onValueChange={setFilterContentType}>
                            <SelectTrigger className="w-[250px]">
                                <SelectValue placeholder="Content Type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Content Types</SelectItem>
                                {contentTypes.map((ct) => (
                                    <SelectItem key={ct.id} value={ct.id.toString()}>
                                        {ct.app_label} | {ct.model}
                                    </SelectItem>
                                ))}
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
                    <CardTitle>Permissions ({permissions.length})</CardTitle>
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
                                    <TableHead>Name</TableHead>
                                    <TableHead>Codename</TableHead>
                                    <TableHead>Content Type</TableHead>
                                    <TableHead>ID</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {permissions.map((permission) => (
                                    <TableRow key={permission.id}>
                                        <TableCell className="font-medium">
                                            <div className="flex items-center gap-2">
                                                <Shield className="h-4 w-4 text-muted-foreground" />
                                                {permission.name}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline">{permission.codename}</Badge>
                                        </TableCell>
                                        <TableCell>{permission.content_type_name}</TableCell>
                                        <TableCell className="text-muted-foreground">#{permission.id}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
