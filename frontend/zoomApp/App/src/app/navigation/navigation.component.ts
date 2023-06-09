import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css'],
})
export class NavigationComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit(): void {}

  goToAboutUs() {
    this.router.navigate(['about']);
  }

  goToMeeting() {
    this.router.navigate(['meeting']);
  }

  goToHome() {
    this.router.navigate(['home']);
  }

  goToPrueba(){
    this.router.navigate(['prueba']);
  }
  goToCharts(){
    this.router.navigate(['charts']);
  }
}
