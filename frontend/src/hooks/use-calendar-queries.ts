import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { calendarApi } from '@/lib/api-client';
import { toast } from 'sonner';

// Query Keys
export const calendarKeys = {
    all: ['calendars'] as const,
    lists: () => [...calendarKeys.all, 'list'] as const,
    list: (filters?: any) => [...calendarKeys.lists(), { filters }] as const,
    details: () => [...calendarKeys.all, 'detail'] as const,
    detail: (id: string) => [...calendarKeys.details(), id] as const,
};

// Queries
export function useCalendars() {
    return useQuery({
        queryKey: calendarKeys.lists(),
        queryFn: calendarApi.getAll,
    });
}

export function useCalendar(id: string) {
    return useQuery({
        queryKey: calendarKeys.detail(id),
        queryFn: () => calendarApi.getById(id),
        enabled: !!id,
    });
}

// Mutations
export function useCreateCalendar() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: calendarApi.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: calendarKeys.lists() });
            toast.success('Calendar created successfully');
        },
        onError: (error: Error) => {
            toast.error(`Failed to create calendar: ${error.message}`);
        },
    });
}

export function useUpdateCalendar() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: any }) =>
            calendarApi.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: calendarKeys.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: calendarKeys.lists() });
            toast.success('Calendar updated successfully');
        },
        onError: (error: Error) => {
            toast.error(`Failed to update calendar: ${error.message}`);
        },
    });
}

export function useDeleteCalendar() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: calendarApi.delete,
        onMutate: async (id: string) => {
            // Cancel outgoing refetches
            await queryClient.cancelQueries({ queryKey: calendarKeys.lists() });

            // Snapshot previous value
            const previousCalendars = queryClient.getQueryData(calendarKeys.lists());

            // Optimistically update
            queryClient.setQueryData(calendarKeys.lists(), (old: any[] = []) =>
                old.filter((calendar) => calendar.ukid !== id)
            );

            return { previousCalendars };
        },
        onError: (error: Error, _, context) => {
            // Rollback on error
            if (context?.previousCalendars) {
                queryClient.setQueryData(calendarKeys.lists(), context.previousCalendars);
            }
            toast.error(`Failed to delete calendar: ${error.message}`);
        },
        onSuccess: () => {
            toast.success('Calendar deleted successfully');
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: calendarKeys.lists() });
        },
    });
}
