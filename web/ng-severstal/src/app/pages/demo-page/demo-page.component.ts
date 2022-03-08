import { Component, OnInit } from '@angular/core';
import {DatepickerOptions} from "ngx-dates-picker";

@Component({
  selector: 'app-demo-page',
  templateUrl: './demo-page.component.html',
  styleUrls: ['./demo-page.component.scss']
})


export class DemoPageComponent implements OnInit {
  public graph = {
    data: [
      { x: [1, 2, 3], y: [2, 6, 3], type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
      { x: [1, 2, 3], y: [2, 5, 3], type: 'bar' },
    ],
    layout: {title: 'A Fancy Plot'}
  };

  productName: string = "хуй";
  date: Date = new Date();
  products: string[] = [
    "Вал",
    "хуй"
  ]
  __datePickerOptions: DatepickerOptions = {
    minDate: new Date(new Date().getFullYear(), new Date().getMonth()),
    maxDate: new Date(2099, 0),
    addStyle: {
      'width': '100%'
    }
  }
  __initialized = false;

  constructor() {

  }

  ngAfterViewInit() {
    this.__initialized = true;
  }

  ngDoCheck() {
    let dateToCompare = new Date();
    dateToCompare.setHours(0, 0, 0, 0);
    this.date.setHours(0, 0, 0, 0);
    if (this.__initialized && this.date < dateToCompare) {
      this.date = new Date();
      alert("Выберите будущую дату")
    }
  }

  ngOnInit(): void {
  }

}
