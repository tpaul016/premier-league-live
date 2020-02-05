import { Component, OnInit, Input } from '@angular/core';
import { CloudData, CloudOptions } from 'angular-tag-cloud-module';


@Component({
  selector: 'match-details',
  templateUrl: './match-details.component.html',
//   styleUrls: ['./app.component.css']
})
export class MatchDetailsComponent implements OnInit {
    @Input() tweetData: any;
    options: CloudOptions = {
        // if width is between 0 and 1 it will be set to the size of the upper element multiplied by the value 
        width: 300,
        height: 400,
        overflow: true,
      };

    ngOnInit() {
    }

}