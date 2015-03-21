package main

import (
       "fmt"
       "flag"
       "os"
       "io"
       "bufio"
       "strings"
       "strconv"
       "math"
)

type Point struct {
     x float64
     y float64
}
func GetDistanceMiles(p1 Point, p2 Point) (miles float64) {

     degree_to_rad := math.Pi/180.0;
     d_lon := (p2.x - p1.x)*degree_to_rad
     d_lat := (p2.y - p1.y)*degree_to_rad
     a:=math.Pow(math.Sin(d_lat/2),2) +
                 math.Cos(p1.y * degree_to_rad) *
                 math.Cos(p2.y * degree_to_rad) *
                 math.Pow(math.Sin(d_lon/2),2)
     c:=2*math.Atan2(math.Sqrt(a),math.Sqrt(1-a))
     miles = 3956 * c
    
     return miles
}


func (p *Point) Set(sx string, sy string){
     p.x,_=strconv.ParseFloat(sx,64)
     p.y,_=strconv.ParseFloat(sy,64)
}
func (p Point) String() string {
     return fmt.Sprintf("%f %f",p.x, p.y)
}

type Track []*Point

func (t Track) Dump(){
     for _,p:=range t{
         fmt.Println(p);
     }
}

func (c Track) IsValid(max_hop_miles float64) (ok bool, dist float64) {
     ok=false
     for i:=1; i<len(c); i++ {
         dist = GetDistanceMiles(*c[i], *c[i-1])
         if(dist > max_hop_miles){
            return
         }
     }
     ok=true
     return 
}
func (c Track) GetSub(start int, stop int) (string){
     if start==stop {
        return ""
     }
     s := "LINESTRING ("
     for i:=start; i<stop; i++{
         if i!= start{
            s+=", "
         }
         s+=c[i].String()
         //s+=fmt.Sprintf("%f %f",c[i].x, c[i].y)
     }
     s+=")"
     return s
}
func (c Track) GetLineStrings() (res []string) {
     prv:=0
     for i:=1; i< len(c); i++ {
         if math.Abs(c[i].x - c[i-1].x) > 100.0 {
            s:=c.GetSub(prv, i-1)
            res = append(res, s)
            prv=i
         }
     }
     s:=c.GetSub(prv,len(c))
     res = append(res,s)
     return
}



func main() {

     var filename = flag.String("file", "", "Input CSV File")
     flag.Parse()
     //fmt.Println(*filename);

     imap:=make(map[string]string)
     tmap:=make(map[string]Track)
     fi,_:=os.Open(*filename)
     r:=bufio.NewReader(fi)
     for line,_,err := r.ReadLine(); err!=io.EOF; line,_,err=r.ReadLine(){
         //fmt.Println(string(line))
         cols := strings.Split(string(line),"\t")
         if cols[0]=="1" {
            id:=cols[1]
            fin:=strings.TrimSpace(cols[2]);
            if fin==""{
               fin = "UNSPECIFIED"
            }
            imap[id] = fin           
            //fmt.Println("\t"+id+"\t"+fin)
         } else if cols[0]=="3" {
            id:=cols[1]            
            //lon:=cols[3]
            //lat:=cols[2]
            var mypoint Point
            mypoint.Set(cols[3], cols[2])
            track,ok := tmap[id]
            if !ok {
               var track Track;
               tmap[id]=append(track, &mypoint)
            } else {
               tmap[id]=append(track, &mypoint) 
            }
         }
     }

     fmt.Println("name\ttype\twkt") 
     for i,v:=range tmap {

         ok,_/*dist*/:=v.IsValid(100)
         if(!ok){
           //fmt.Println("Bad ",i," Distance is ",dist) 
           continue
         }
      
         s,ok := imap[i]
           if !ok {           
            s="UNKNOWN"
         }
         //v.Dump()
         //fmt.Println()
         
         lines:=v.GetLineStrings()
         for _,ls := range lines {
                  fmt.Println(i+"\t"+s+"\t"+ls)
         }
     }

}
