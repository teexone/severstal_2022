import {ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {DataService} from "../../services/data.service";
import {MatCheckboxChange} from "@angular/material/checkbox";
import {PlotlyService} from "angular-plotly.js";

@Component({
  selector: 'app-demo-page',
  templateUrl: './demo-page.component.html',
  styleUrls: ['./demo-page.component.scss']
})


export class DemoPageComponent implements OnInit {

  __initialized = false;
  capturedResources: { name: string, alias: string, active: boolean }[] = [];
  currentMethod: string = "linear";
  date: Date = new Date();
  indicesPlot: any = {
    data: [],
    layout: {
      showlegend: true,
      paper_bgcolor: '#F2F2F2FF',
      plot_bgcolor: '#F2F2F2FF',
      title: 'Динамика цен на другие товары',
      width: 500,
      height: 500,
      margin: {
        t: 50
      }
    }
  };
  @ViewChild('IndicesPlotContainer') indicesPlotContainer!: ElementRef;
  methods: { name: string, alias: string, id: number }[] = [
    {name: "Линейная", alias: 'linear', id: 1},
    {name: "Квадратичная", alias: 'quadratic', id: 2},
    {name: "Кубическая", alias: 'cubic', id: 3},
    {name: "Экспоненциальная", alias: 'exponential', id: 4},
  ]
  minDate = new Date();
  price?: {
    left: number,
    right: number
  };
  priceLowerPlot = {
    layout: {
      type: 'line',
      xref: 'paper',
      x0: 0,
      y0: 12.0,
      x1: 1,
      y1: 12.0,
      line: {
        color: 'rgb(255, 0, 0)',
        width: 4,
        dash: 'dot'
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
      datarevision: 0,
      margin: {
        t: 50
      },
      shapes: [{
        type: 'rect',
        xref: 'paper',
        x0: 0,
        y0: 12.0,
        x1: 1,
        y1: 12.0,
        fillcolor: 'rgba(7, 99, 0, .5)',
        line: {
          color: 'rgba(7, 99, 0, .5)',
          width: 1,
        }
      }
      ]
    }
  };

  @ViewChild('PricePlotContainer') pricesPlotContainer!: ElementRef;
  probability?: number;
  productName: string = "Колесо 3519.05.02.006";
  products!: string[];
  resources: { name: string, alias: string, active: boolean }[] = []

  constructor(public data: DataService, public cd: ChangeDetectorRef, public plotly: PlotlyService) {
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

  calculate() {
    this.data.calculate(this.productName, this.resources.filter(x => x.active).map(x => x.alias),
      this.currentMethod,
      this.date).then(x => {
      console.log('hello')
      this.price = {
        left: typeof x.left == 'number' ? x.left : parseInt(x.left),
        right: typeof x.right == 'number' ? x.right : parseInt(x.right)
      };
      this.pricePlot.layout.shapes[0].y0 = this.price.left;
      this.pricePlot.layout.shapes[0].y1 = this.price.right;
      this.pricePlot = {...this.pricePlot};
      this.cd.detectChanges();
      this.pricePlot.layout.datarevision++;
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
            mode: 'points',
            x: data.x.map((i: any) => new Date(i * 1000)),
            y: data.y,
          })
        })
      }
    }
  }

  check($event: MatCheckboxChange, r: any) {
    r.active = $event.checked
  }

  download() {
    this.data.downloadFile(this.productName, this.resources.filter(x => x.active).map(x => x.alias), this.currentMethod, this.date)
  }

  getPrice() {
    return {
      left: Math.round(Math.min(this.price!.left, this.price!.right)),
      right: Math.round(Math.max(this.price!.left, this.price!.right)),
    };
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
