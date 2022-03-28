import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";

const static_address = "http://20.101.115.80:5000/"
//const static_address = "http://localhost:5000/"


@Injectable({
  providedIn: 'root'
})
export class DataService {
  constructor(public http: HttpClient) {

  }

  async calculate(name: string, indices: string[], method: string, date: Date) {
    return new Promise<{ [p: string]: any }>(((resolve, reject) => {
      this.http.get(static_address + "calculate", {
        params: {
          'product': name,
          'include': indices,
          'date': date.getTime(),
        }
      }).subscribe((data) => {
        resolve(data);
      })
    }));
  }

  async downloadFile(name: string, indices: string[], method: string, date: Date) {
    this.http.get(static_address + "calculate", {
      responseType: "blob",
      params: {
        'product': name,
        'include': indices,
        'date': date.getTime(),
        'method': method,
        'to_excel': true,
      }
    })
      .subscribe(data => {
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(data)
        a.href = objectUrl
        a.download = "Prediction_" + Date() + '.xlsx'
        a.click()
        URL.revokeObjectURL(objectUrl)
      });
  }

  async getDataPlot(product: string) {
    return new Promise<{ [p: string]: any }>(((resolve, reject) => {
      this.http.get(static_address + "plot", {params: {product, what: 'price'}}).subscribe((data) => {
        resolve(data);
      })
    }));
  }

  async getIndexPlot(index: string) {
    return new Promise<{ [p: string]: any }>(((resolve, reject) => {
      this.http.get(static_address + "plot", {params: {index: index, what: 'index'}}).subscribe((data) => {
        resolve(data);
      })
    }));
  }

  async getIndices() {
    return new Promise<{ [p: string]: any }>(((resolve, reject) => {
      this.http.get<{ toplist: string[] }>(static_address + "indices").subscribe(data => resolve(data));
    }));
  }

  async getTop() {
    return new Promise<{ [p: string]: any }>(((resolve, reject) => {
      this.http.get<{ toplist: string[] }>(static_address + "top").subscribe(data => resolve(data));
    }));
  }
}


