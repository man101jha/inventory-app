import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { InventoryItem } from '../models/inventory-item.model';

import { environment } from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class InventoryService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    getItems(): Observable<InventoryItem[]> {
        return this.http.get<InventoryItem[]>(`${this.apiUrl}/products`);
    }

    getItem(id: number): Observable<InventoryItem> {
        return this.http.get<InventoryItem>(`${this.apiUrl}/product/${id}`);
    }

    addItem(item: Omit<InventoryItem, 'id'>): Observable<InventoryItem> {
        return this.http.post<InventoryItem>(`${this.apiUrl}/product`, item);
    }

    updateItem(updatedItem: InventoryItem): Observable<any> {
        return this.http.put(`${this.apiUrl}/product/${updatedItem.id}`, updatedItem);
    }

    deleteItem(id: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}/product/${id}`);
    }
}
