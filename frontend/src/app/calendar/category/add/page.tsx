"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, Suspense } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useCreateCategory, useUpdateCategory, useCategory } from "@/hooks/use-category-queries";

const categorySchema = z.object({
    name: z.string().min(1, "Category name is required"),
    color: z.string().regex(/^#[0-9A-F]{6}$/i, "Must be a valid hex color"),
    description: z.string().optional(),
});

type CategoryFormValues = z.infer<typeof categorySchema>;

function AddCategoryForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const id = searchParams.get("id");
    const isEditMode = !!id;

    const createCategory = useCreateCategory();
    const updateCategory = useUpdateCategory();
    const { data: categoryData, isLoading: isLoadingCategory } = useCategory(id ? parseInt(id) : 0);

    const { register, handleSubmit, formState: { errors }, reset, setValue } = useForm<CategoryFormValues>({
        resolver: zodResolver(categorySchema),
        defaultValues: {
            name: "",
            color: "#000000",
            description: ""
        }
    });

    useEffect(() => {
        if (isEditMode && categoryData) {
            reset({
                name: categoryData.name,
                color: categoryData.color,
                description: categoryData.description || ""
            });
        }
    }, [isEditMode, categoryData, reset]);

    const onSubmit = (data: CategoryFormValues) => {
        if (isEditMode && id) {
            updateCategory.mutate({ id: parseInt(id), data }, {
                onSuccess: () => {
                    router.push("/calendar/category/list");
                }
            });
        } else {
            createCategory.mutate(data, {
                onSuccess: () => {
                    router.push("/calendar/category/list");
                }
            });
        }
    };

    if (isEditMode && isLoadingCategory) {
        return <div>Loading...</div>;
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>{isEditMode ? "Edit Category" : "Add New Category"}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="name">Category Name</Label>
                        <Input
                            id="name"
                            {...register("name")}
                            placeholder="e.g. Work, Personal"
                        />
                        {errors.name && <p className="text-sm text-red-500">{errors.name.message}</p>}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="color">Color Code</Label>
                        <div className="flex gap-2">
                            <Input
                                id="color"
                                type="color"
                                {...register("color")}
                                className="w-12 h-10 p-1"
                            />
                            <Input
                                {...register("color")}
                                placeholder="#000000"
                                className="flex-1"
                            />
                        </div>
                        {errors.color && <p className="text-sm text-red-500">{errors.color.message}</p>}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="description">Description</Label>
                        <Textarea
                            id="description"
                            {...register("description")}
                            placeholder="Optional description"
                        />
                    </div>

                    <Button type="submit" className="w-full" disabled={createCategory.isPending || updateCategory.isPending}>
                        {createCategory.isPending || updateCategory.isPending ? "Saving..." : (isEditMode ? "Update Category" : "Create Category")}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
}

export default function AddCategoryPage() {
    return (
        <div className="max-w-xl mx-auto">
            <Suspense fallback={<div>Loading...</div>}>
                <AddCategoryForm />
            </Suspense>
        </div>
    );
}
