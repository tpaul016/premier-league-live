import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {animate, state, style, transition, trigger} from '@angular/animations';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ])
  ]
})
export class AppComponent implements OnInit{
  title = 'premier-league-live';
  private apiUrl = 'http://127.0.0.1:5000/';
  matches;
  spin: boolean = false;
  columnsToDisplay = ['Date', 'Home Team', 'Away Team', 'Keyword'];
  expandedElement: any | null;

  constructor(private http: HttpClient) {
  }

  ngOnInit() {
    this.getGameSchedules();
  }

  getGameSchedules() {
    this.http.get(this.apiUrl + 'schedule?dateTo=2020-02-04').subscribe(data =>{
      this.matches = data;
      this.matches = this.matches.reverse();
    })
  }

  getTweetData(keyword, date, element) {
    this.spin = true;
    this.http.get(this.apiUrl + 'tweetTopics?keyword=' + keyword + '&date=' + date).subscribe(data => {
      this.spin = false;
      element.tweetTopics = data;
    },
    err => {
      this.spin = false;
      console.log(err.message);
    })
  }

}
