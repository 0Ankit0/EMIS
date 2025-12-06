"use client";

import { Button } from "@/components/ui/button";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Edit, Eye, Trash2, Plus } from "lucide-react";
import Link from "next/link";
import { useCategories, useDeleteCategory } from "@/hooks/use-category-queries";
import type { Category } from "@/types/calendar";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";



export default function CategoryListPage() {
    const { data: categories = [], isLoading } = useCategories();
    const deleteCategory = useDeleteCategory();

    const handleDelete = (id: string) => {
        if (!confirm("Are you sure you want to delete this category?")) return;
        deleteCategory.mutate(id);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">Categories</h1>
                <Button asChild>
                    <Link href="/calendar/category/add">
                        <Plus className="mr-2 h-4 w-4" /> Add Category
                    </Link>
                </Button>
            </div>

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Name</TableHead>
                            <TableHead>Color</TableHead>
                            <TableHead>Description</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-4">Loading...</TableCell>
                            </TableRow>
                        ) : categories.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-4">No categories found</TableCell>
                            </TableRow>
                        ) : (
                            categories.map((category: Category) => (
                                <TableRow key={category.ukid}>
                                    <TableCell className="font-medium">{category.name}</TableCell>
                                    <TableCell>
                                        <div className="flex items-center gap-2">
                                            <div
                                                className="w-6 h-6 rounded border"
                                                style={{ backgroundColor: category.color }}
                                            />
                                            <span className="text-sm text-muted-foreground">{category.color}</span>
                                        </div>
                                    </TableCell>
                                    <TableCell>{category.description || "—"}</TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Dialog>
                                                <DialogTrigger asChild>
                                                    <Button variant="ghost" size="icon" title="View">
                                                        <Eye className="h-4 w-4" />
                                                    </Button>
                                                </DialogTrigger>
                                                <DialogContent>
                                                    <DialogHeader>
                                                        <DialogTitle>{category.name}</DialogTitle>
                                                        <DialogDescription>Category Details</DialogDescription>
                                                    </DialogHeader>
                                                    <div className="space-y-4 pt-4">
                                                        <div className="flex items-center gap-2">
                                                            <div
                                                                className="w-8 h-8 rounded border"
                                                                style={{ backgroundColor: category.color }}
                                                            />
                                                            <span className="font-mono">{category.color}</span>
                                                        </div>
                                                        {category.description && (
                                                            <div className="space-y-1">
                                                                <h4 className="text-sm font-medium">Description</h4>
                                                                <p className="text-sm text-muted-foreground">{category.description}</p>
                                                            </div>
                                                        )}
                                                    </div>
                                                </DialogContent>
                                            </Dialog>
                                            <Button variant="ghost" size="icon" title="Edit" asChild>
                                                <Link href={`/calendar/category/add?id=${category.ukid}`}>
                                                    <Edit className="h-4 w-4" />
                                                </Link>
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                title="Delete"
                                                className="text-destructive hover:text-destructive"
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleDelete(category.ukid);
                                                }}
                                                disabled={deleteCategory.isPending}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
}
