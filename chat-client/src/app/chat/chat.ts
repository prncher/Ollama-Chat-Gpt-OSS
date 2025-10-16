import { Component, HostListener, Input, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

export interface ChatMessage {
  id: number;
  message: string;
}

@Component({
  selector: 'Chat',
  imports: [FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css'
})
export class Chat implements OnInit {
  @Input() id: number | undefined;
  private socket: WebSocket | undefined;
  messages: ChatMessage[] = [];
  chatMessage: string = '';
  showOverlay = false;

  ngOnInit(): void {
    if (!this.id) {
      return
    }
    this.socket = new WebSocket(`ws://localhost:5600/ws/${this.id}`);
    if (this.socket) {
      this.socket.onmessage = (msgEvt: MessageEvent<string>) => {
        this.messages = [...this.messages, { id: this.messages.length + 1, message: msgEvt.data }];
        this.showOverlay = false
      }
    }


  }
  sendChatMessage() {
    if (this.chatMessage && this.socket) {
      this.messages = [...this.messages, { id: this.messages.length + 1, message: `Question: ${this.chatMessage}` }];
      this.socket.send(this.chatMessage)
      this.showOverlay = true
      this.chatMessage = ''
    }
  }


  @HostListener('document:keyup.enter', ['$event'])
  handleEnterKey(event: Event) {
    const keyboardEvent: KeyboardEvent = event as KeyboardEvent
    if (keyboardEvent && keyboardEvent.key === 'Enter') {
      this.sendChatMessage()
    }
  }
}
