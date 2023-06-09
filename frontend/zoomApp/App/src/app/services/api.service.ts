import { Injectable } from '@angular/core';
import { Firestore, collection, addDoc } from '@angular/fire/firestore';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private BASE_URL = 'http://localhost:5000/';
  constructor(private client: HttpClient) {}

  getUserAPI(): Observable<any> {
    return this.client.get(this.BASE_URL + 'user');
  }
  getUserLogin(user: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'login', user);
  }
  registerUser(user: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'register', user);
  }
  registerAdmin(admin: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'adminRegister', admin);
  }
  createServiceWithUser(service: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'service', service);
  }
  getServices(username: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'userServices', username);
  }

  getAllServices(): Observable<any> {
    return this.client.get(this.BASE_URL + 'adminServices');
  }

  getServicesById(id: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'serviceById', id);
  }
  getProceduresByPhase(phase: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'servicePhase', phase);
  }

  newPhaseProcedure(procedure: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'newProcedure', procedure);
  }
  getProcedureById(id: any): Observable<any> {
    return this.client.post(this.BASE_URL + 'procedureById', id);
  }

  getHelloFromBackend(): Observable<any> {
    return this.client.get(this.BASE_URL + 'hello');
  }
}
