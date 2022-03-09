import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {DatepickerOptions} from "ngx-dates-picker";
import {DataService} from "../../services/data.service";
import {FormGroup} from "@angular/forms";
import {MatCheckboxChange} from "@angular/material/checkbox";

@Component({
  selector: 'app-demo-page',
  templateUrl: './demo-page.component.html',
  styleUrls: ['./demo-page.component.scss']
})


export class DemoPageComponent implements OnInit {

  @ViewChild('IndicesPlotContainer') indicesPlotContainer!: ElementRef;
  @ViewChild('PricePlotContainer') pricesPlotContainer!: ElementRef;

  indicesPlot: any = {
    data: [],
    layout: {
      showlegend: true,
      paper_bgcolor: '#F2F2F2FF',
      plot_bgcolor:'#F2F2F2FF',
      title: 'Динамика цен на другие товары',
      width: 500,
      height: 500,
      margin: {
        t: 50
      }
    }
  };

  pricePlot = {
    data: [] as any[],
    layout: {
      title: 'Изменение цены',
      paper_bgcolor: '#F2F2F2FF',
      plot_bgcolor: '#F2F2F2FF',
      width: 500,
      height: 500,
      margin: {
        t: 50
      }
    }
  };

  productName: string = "Колесо 3519.05.02.006";
  minDate = new Date();
  date: Date = new Date();
  products!: string[];
  capturedResources: { name: string, alias: string, active: boolean }[] = [];

  methods: { name: string, alias: string, id: number }[] = [
    {name: "Линейная", alias: 'linear', id: 1 },
    {name: "Квадратичная", alias: 'quadratic', id: 2 },
    {name: "Кубическая", alias: 'cubic', id: 3 },
    {name: "Экспоненциальная", alias: 'exponential', id: 4 },
  ]

  currentMethod: string = "linear";
  price?: number;
  probability?: number;

  getPrice() {
    return this.price ? Math.round(this.price) : undefined;
  }
  resources: { name: string, alias: string, active: boolean }[] = []

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
      this.data.getIndices().then(body => {
        const indices = body.indices
        for (let index in indices) {
          this.resources.push({
            name: index,
            alias: indices[index],
            active: false,
          })
        }
      });

  }
  check($event: MatCheckboxChange, r: any) {
    r.active = $event.checked
  }

  calculate() {
    this.data.calculate(this.productName, this.resources.filter(x => x.active).map(x => x.alias),
      this.currentMethod,
      this.date).then(x => {
        this.probability = x.error;
        this.price = x.predicted;
      });
    this.data.getDataPlot(this.productName).then(data => {
      data.x = data.x.map((i: any) => new Date(i * 1000))
      this.pricePlot.data = [data]
    });
    this.indicesPlot.data = []
    for (let index of this.resources) {
      if (index.active) {
        this.data.getIndexPlot(index.alias).then(data => {
          this.indicesPlot.data.push({
            name: index.name,
            type: 'scatter',
            mode: 'lines+points',
            x: data.x.map((i: any) => new Date(i * 1000)),
            y: data.y,
          })
        })
      }
    }
  }

  download() {
    this.data.downloadFile(this.productName, this.resources.filter(x => x.active).map(x => x.alias), this.currentMethod, this.date)
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
    if (this.indicesPlotContainer && this.pricesPlotContainer) {
      this.pricePlot.layout.width = this.pricesPlotContainer.nativeElement.getBoundingClientRect().width * 0.95
      this.pricePlot.layout.height = this.pricesPlotContainer.nativeElement.getBoundingClientRect().height * 0.95
      this.indicesPlot.layout.width = this.indicesPlotContainer.nativeElement.getBoundingClientRect().width * 0.95
      this.indicesPlot.layout.height = this.indicesPlotContainer.nativeElement.getBoundingClientRect().height * 0.95
    }
  }

  ngOnInit(): void {

  }
}
