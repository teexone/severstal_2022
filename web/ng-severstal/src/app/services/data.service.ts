import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class DataService {
  constructor(public http: HttpClient) {

  }
  async getTop(){
    return new Promise<{[p: string]: any}>(((resolve, reject) => {
      this.http.get("http://10.91.55.214:5000").subscribe((top) => {
        resolve(top);
      })
    }));
  }
  async getData(){
    return new Promise<{[p: string]: any}>(((resolve, reject) => {
      this.http.get("http://:5000").subscribe((data) => {
         resolve(data);
      })
    }));
  }
}


