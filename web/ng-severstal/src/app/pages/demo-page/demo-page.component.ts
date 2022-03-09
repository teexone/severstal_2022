import { Component, OnInit } from '@angular/core';
import {DatepickerOptions} from "ngx-dates-picker";
import {MatCheckboxModule} from '@angular/material/checkbox';
import {DataService} from "../../services/data.service";
import {FormGroup} from "@angular/forms";

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

  productName: string = "Колесо 3519.05.02.006";

  date: Date = new Date();
  products!: string[];
  currentMethod: string = "Линейная";
  methods: string[] = [
    "Линейная",
    "Квадратичная",
    "Кубическая",
    "Экспоненциальная",
    "С наименьшей LSE"
  ]
  resources: string[] = [
    "Сталь",
    "Бензин",
    "Дизель",
    "Станки",
    "Автотранспорт",
    "Железная руда",
    "Стальной прокат",
    "Стальные профили",
    "Цельнокатаные колёса"
  ]

  __datePickerOptions: DatepickerOptions = {
    minDate: new Date(new Date().getFullYear(), new Date().getMonth()),
    maxDate: new Date(2099, 0),
    addStyle: {
      'width': '100%'
    }
  }
  __initialized = false;

  constructor(public data: DataService) {
      this.data.getTop().then(body => this.products = body.toplist);
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
