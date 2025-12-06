import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { categoryApi } from '@/lib/api-client';
import { toast } from 'sonner';

// Query Keys
export const categoryKeys = {
    all: ['categories'] as const,
    lists: () => [...categoryKeys.all, 'list'] as const,
    list: (filters?: any) => [...categoryKeys.lists(), { filters }] as const,
    details: () => [...categoryKeys.all, 'detail'] as const,
    detail: (id: string) => [...categoryKeys.details(), id] as const,
};

// Queries
export function useCategories() {
    return useQuery({
        queryKey: categoryKeys.lists(),
        queryFn: categoryApi.getAll,
    });
}

export function useCategory(id: string) {
    return useQuery({
        queryKey: categoryKeys.detail(id),
        queryFn: () => categoryApi.getById(id),
        enabled: !!id,
    });
}

// Mutations
export function useCreateCategory() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: categoryApi.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: categoryKeys.lists() });
            toast.success('Category created successfully');
        },
        onError: (error: Error) => {
            toast.error(`Failed to create category: ${error.message}`);
        },
    });
}

export function useUpdateCategory() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: any }) =>
            categoryApi.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: categoryKeys.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: categoryKeys.lists() });
            toast.success('Category updated successfully');
        },
        onError: (error: Error) => {
            toast.error(`Failed to update category: ${error.message}`);
        },
    });
}

export function useDeleteCategory() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: categoryApi.delete,
        onMutate: async (id) => {
            await queryClient.cancelQueries({ queryKey: categoryKeys.lists() });
            const previousCategories = queryClient.getQueryData(categoryKeys.lists());

            queryClient.setQueryData(categoryKeys.lists(), (old: any[] = []) =>
                old.filter((category) => category.ukid !== id)
            );

            return { previousCategories };
        },
        onError: (error: Error, _, context) => {
            if (context?.previousCategories) {
                queryClient.setQueryData(categoryKeys.lists(), context.previousCategories);
            }
            toast.error(`Failed to delete category: ${error.message}`);
        },
        onSuccess: () => {
            toast.success('Category deleted successfully');
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: categoryKeys.lists() });
        },
    });
}
