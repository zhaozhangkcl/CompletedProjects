#ifndef KNIGHTS_H
#define KNIGHTS_H

#include <utility>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iostream>
#include <cstdint>

using std::pair;
using std::make_pair;
using std::vector;
using std::find;
typedef vector<pair<int,int> > Path;

/** Helper function: adds two pairs of ints */
 /*
pair<int,int> operator+(const pair<int,int> & a, const pair<int,int> & b) {
    return make_pair(a.first + b.first, a.second + b.second);
}
*/
// TODO - your code goes here
/* this function takes an argument of position on the board and returns all the possible position
in anticlockwise order*/
 Path move(pair<int,int> input) {
  //create a container Path which will be returned
  Path moves;
  //add the 6 clock position to the container
 moves.push_back(make_pair(input.first-1, input.second-2));
  // add postions
  moves.push_back(make_pair(input.first+1, input.second-2));
  //add positions
moves.push_back(make_pair(input.first+2, input.second-1));
  //add postiions
moves.push_back(make_pair(input.first+2, input.second+1));
  //add positions
moves.push_back(make_pair(input.first+1, input.second+2));
  //add positions
moves.push_back(make_pair(input.first-1, input.second+2));
  //add positions
moves.push_back(make_pair(input.first-2, input.second+1));
  //add positions
moves.push_back(make_pair(input.first-2, input.second-1));
  //return container
  return moves;
}

/*this function finds all the possible legal squares can reached by a knight
which are not in the path */
 vector<pair<int, int>> legal_moves(int boardSize, Path p, pair<int, int> pos) {
     //enuerate all the different moves a knight can make in this pos
     Path moves = move(pos);
     Path value;
     for (auto legalMove : moves) {
         if ((legalMove.first >= 0 && legalMove.second >= 0) && 
             (legalMove.first < boardSize&& legalMove.second < boardSize) && 
             (!(find(p.begin(), p.end(), legalMove) != p.end()))) 
         {
             value.push_back(legalMove);
         }

        

         /*
         if ) {
             value.push_back(legalMove);
         }
         */
     }

     

    
     
     return value;
 }

/*recursive method search for a tour within he boardSize */
pair<Path,bool> first_tour(int boardSize, Path p) {
  //base case if the p's length equal boardSize
    //check if p is non-empty
    if (p.size() == boardSize * boardSize) {
      
        return make_pair(p, true);
    }
    pair<int, int> lastElement = p.back();
    
  Path legalMoves = legal_moves(boardSize, p, lastElement);
  for(auto legalMove : legalMoves) {
     
     
    p.push_back(legalMove);
    
    auto tour = first_tour(boardSize, p); 
    if (tour.first.size() == boardSize * boardSize) {
        return tour;
    }

}
  return make_pair(Path(),false);

 // order may need to reverse

  //recursive step,

}















// Do not edit below this line

#endif
