import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { eventApi } from '@/lib/api-client';
import { toast } from 'sonner';

// Query Keys
export const eventKeys = {
    all: ['events'] as const,
    lists: () => [...eventKeys.all, 'list'] as const,
    list: (filters?: Record<string, string>) => [...eventKeys.lists(), { filters }] as const,
    details: () => [...eventKeys.all, 'detail'] as const,
    detail: (id: string) => [...eventKeys.details(), id] as const,
};

// Queries
export function useEvents(filters?: Record<string, string>) {
    return useQuery({
        queryKey: eventKeys.list(filters),
        queryFn: () => eventApi.getAll(filters),
    });
}

export function useEvent(id: string) {
    return useQuery({
        queryKey: eventKeys.detail(id),
        queryFn: () => eventApi.getById(id),
        enabled: !!id,
    });
}

// Mutations
export function useCreateEvent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: eventApi.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: eventKeys.lists() });
            toast.success('Event created successfully');
        },
        onError: (error: Error) => {
            toast.error(`Failed to create event: ${error.message}`);
        },
    });
}

export function useUpdateEvent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: any }) =>
            eventApi.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: eventKeys.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: eventKeys.lists() });
            toast.success('Event updated successfully');
        },
        onError: (error: Error) => {
            toast.error(`Failed to update event: ${error.message}`);
        },
    });
}

export function useLinkEvent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, calendarId }: { id: string; calendarId: number }) =>
            eventApi.update(id, { calendar: calendarId }),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: eventKeys.lists() });
            toast.success('Event linked successfully');
        },
        onError: (error: Error) => {
            toast.error(`Failed to link event: ${error.message}`);
        },
    });
}

export function useDeleteEvent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: eventApi.delete,
        onMutate: async (id) => {
            await queryClient.cancelQueries({ queryKey: eventKeys.lists() });
            const previousEvents = queryClient.getQueryData(eventKeys.lists());

            queryClient.setQueryData(eventKeys.lists(), (old: any[] = []) =>
                old.filter((event) => event.ukid !== id)
            );

            return { previousEvents };
        },
        onError: (error: Error, _, context) => {
            if (context?.previousEvents) {
                queryClient.setQueryData(eventKeys.lists(), context.previousEvents);
            }
            toast.error(`Failed to delete event: ${error.message}`);
        },
        onSuccess: () => {
            toast.success('Event deleted successfully');
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: eventKeys.lists() });
        },
    });
}
