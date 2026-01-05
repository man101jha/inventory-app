export interface InventoryItem {
    id: number;
    name: string;
    category: string;
    quantity: number;
    price: number;
    status: 'In Stock' | 'Low Stock' | 'Out of Stock';
    description?: string;
}
