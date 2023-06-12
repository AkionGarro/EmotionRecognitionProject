import { Injectable } from '@angular/core';
import { Firestore, collection, addDoc } from '@angular/fire/firestore';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private BASE_URL = 'http://localhost:5000/';
  constructor(private client: HttpClient) {}

  sortImageAttention(image: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'sortImage', image);
  }

  getChartsInfo(value: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'getInfoCharts', value);
  }
}
