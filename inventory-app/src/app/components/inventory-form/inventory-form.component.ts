import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { InventoryService } from '../../services/inventory.service';
import { InventoryItem } from '../../models/inventory-item.model';

@Component({
  selector: 'app-inventory-form',
  templateUrl: './inventory-form.component.html',
  styleUrls: ['./inventory-form.component.css']
})
export class InventoryFormComponent implements OnInit {
  inventoryForm: FormGroup;
  isEditMode = false;
  itemId?: number;

  constructor(
    private fb: FormBuilder,
    private inventoryService: InventoryService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.inventoryForm = this.fb.group({
      id: ['', Validators.required],
      name: ['', Validators.required],
      category: ['', Validators.required],
      quantity: [0, [Validators.required, Validators.min(0)]],
      price: [0, [Validators.required, Validators.min(0)]],
      status: ['In Stock', Validators.required],
      description: ['']
    });
  }

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.isEditMode = true;
      this.itemId = Number(idParam);
      this.inventoryService.getItem(this.itemId).subscribe({
        next: (item) => this.inventoryForm.patchValue(item),
        error: () => this.router.navigate(['/inventory'])
      });
    }
  }

  onSubmit(): void {
    if (this.inventoryForm.valid) {
      const formValue = this.inventoryForm.value;

      // Auto-update status based on quantity if desirable, or let user pick.
      // For now, respect user pick or logic? Let's just keep simple.

      let obs$;
      if (this.isEditMode && this.itemId) {
        const updatedItem: InventoryItem = {
          id: this.itemId,
          ...formValue
        };
        obs$ = this.inventoryService.updateItem(updatedItem);
      } else {
        obs$ = this.inventoryService.addItem(formValue);
      }

      obs$.subscribe({
        next: () => this.router.navigate(['/inventory']),
        error: (err: any) => console.error('Error saving item', err)
      });
    }
  }

  onCancel(): void {
    this.router.navigate(['/inventory']);
  }
}
