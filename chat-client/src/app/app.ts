import { Component, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatService } from './chat-service';
import { Chat } from './chat/chat';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,Chat],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  chatService = inject(ChatService)
  protected readonly title = signal('chat-client-angular');
}

