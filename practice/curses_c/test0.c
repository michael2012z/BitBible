#include <ncurses.h>

void test_print() {
  int y = 5, x = 5;
  initscr();
  printw("Hello!");
  move(y, x);
  printw("Hello again!");
  refresh();
  getch();
  endwin();
}

void test_window() {
  initscr();

  int y = 10, x = 20;
  int h = 10, w = 60;

  WINDOW * win = newwin(h, w, y, x);
  refresh();
  box(win, 0, 0);
  mvwprintw(win, 1, 1, "abc");
  wrefresh(win);
  
  getch();

  endwin();
}

void test_window_border() {
  initscr();

  int y = 10, x = 20;
  int h = 10, w = 60;

  WINDOW * win = newwin(h, w, y, x);
  refresh();
  //  box(win, '*', '#');
  //  wborder(win, 0,0,0,0,0,0,0,0);
  wborder(win, '/','\\','+','-','*','*','*','*');
  mvwprintw(win, 1, 1, "abc");
  wrefresh(win);
  
  getch();

  endwin();
}

void test_colors() {
  initscr();

  int y = 10, x = 20;
  int h = 10, w = 60;

  WINDOW * win = newwin(h, w, y, x);
  refresh();
  box(win, 0, 0);
  if (!has_colors())
	mvwprintw(win, 1, 1, "abc");
  else {
	start_color();
	init_pair(1, COLOR_CYAN, COLOR_RED);
	init_pair(2, COLOR_YELLOW, COLOR_BLUE);
	wattron(win, COLOR_PAIR(1));
	mvwprintw(win, 1, 1, "a cyan-on-red hello");
	wattroff(win, COLOR_PAIR(1));
	wattron(win, COLOR_PAIR(2));
	mvwprintw(win, 2, 1, "a yellow-on-blue hello");
	wattroff(win, COLOR_PAIR(2));

  }
  
  wrefresh(win);
  
  getch();

  endwin();
}

void test_layout_basic() {
  initscr();

  int y = 10, x = 20;
  int begx, begy, maxx, maxy;
  
  getyx(stdscr, y, x);
  getbegyx(stdscr, begy, begx);
  getmaxyx(stdscr, maxy, maxx);

  WINDOW * win = newwin(maxy, maxx, 0, 0);
  //  box(win, 0, 0);
  wborder(win, 0,0,0,0,0,0,0,0);
  refresh();
  wrefresh(win);
  
  getch();

  endwin();
}

void test_layout_advanced() {
  initscr();

  int scr_h, scr_w;
  
  getmaxyx(stdscr, scr_h, scr_w);

  int win2_h = scr_h / 3, win2_w = scr_w / 3;
  int win0_h = scr_h - win2_h, win0_w = win2_w;
  int win1_h = win0_h, win1_w = scr_w - win0_w;
  int win3_h = win2_h, win3_w = win1_w;
  
  WINDOW * win0 = newwin(win0_h, win0_w, 0, 0);
  wborder(win0, 0,0,0,0,0,0,0,0);
  WINDOW * win1 = newwin(win1_h, win1_w, 0, win0_w);
  wborder(win1, 0,0,0,0,0,0,0,0);
  WINDOW * win2 = newwin(win2_h, win2_w, win0_h, 0);
  wborder(win2, 0,0,0,0,0,0,0,0);
  WINDOW * win3 = newwin(win3_h, win3_w, win0_h, win0_w);
  wborder(win3, 0,0,0,0,0,0,0,0);

  refresh();
  wrefresh(win0);
  wrefresh(win1);
  wrefresh(win2);
  wrefresh(win3);
  
  getch();

  endwin();
}

int main () {
  test_layout_advanced();
  //  test_layout_basic();
  //  test_colors();
  //  test_window_border();
  //  test_window();
  //  test_print();
  return 0;
}
