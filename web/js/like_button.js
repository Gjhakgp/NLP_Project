'use strict';

const e = React.createElement;
const parent_url=""
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: true,files:[],file_data:[] };
  }
  helper(data){
    let temp=[]
    let temp1=[]
    console.log(data)
    data.forEach(elem=>{
      var regex = /\d+/g;
      var matches = elem.match(regex);
      let bn=parseInt(matches[0])
      // console.log("assss",bn)
      temp.push(bn)
    })
    // temp.sort()
    temp.sort(function(a, b){
      return a - b;
    });
    console.log(temp);
    temp.forEach(elem=>{
      let kn="file"+elem.toString()+".xml"
      // console.log(kn)
      temp1.push(kn)
    })
    this.setState({files:temp1})
  }
  async componentDidMount(){
    // const response=await fetch(parent_url+"get/files?lang=en&tag=all")
    // const data=await response.json()
    let data=await fetch(parent_url+"get/files?lang=en&tag=all").then(response=>response.json()).then(json=>this.helper(json))
  }
  async handleClick(e){
    console.log(e);
    await fetch(parent_url+"get/data?filename="+e).then(response=>response.json()).then(json=>this.setState({file_data:json}))
  }
  getsidenav(){
    let f=this.state.files;
    let ret=[]
    if(f.length==0){
      return(<p></p>)
    }else{
     ret=f.map(el=>(<div><button class="btn btn-primary" onClick={() => this.handleClick(el)}>{el}</button></div>))
     return ret;
  }
}
getmainbody(){
  let f=this.state.file_data;
  let ret=[]
  if(f.length==0){
    return(<p></p>)
  }else{
    ret.push(<h1>{f["event_type"][0]}</h1>)
    ret.push(<p>{f["content"]}</p>)
    let temp1=f["args"]["CASUALTIES-ARG"]
    let str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"CASUALTIES-arg"}<p>{str1}</p></div>)
    temp1=f["args"]["PLACE-ARG"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"PLACE-arg"}<p>{str1}</p></div>)
    temp1=f["args"]["TIME-ARG"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"TIME-arg"}<p>{str1}</p></div>)


    temp1=f["model_data"]["what"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"what-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["when"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"when-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["where"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"where-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["who"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"who-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["why"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div>{"why-arg"}<p>{str1}</p></div>)
    let ret1=ret.map(e=><div>{e}</div>)
    return ret1;
  }
}
  render() {
    // console.log(this.state.files)
    let sidenavx=this.getsidenav()
    let mainbody1=this.getmainbody()
    let temp1=[<div id="sidenav1" class="overflow-auto h-50 m-2">{sidenavx}</div>,<div id="mainbody" class="col-lg">{mainbody1}</div>]
    let temp=[<div class="row">{temp1.map(elem=>elem)}</div>];
    var st2={height: "500px"}
    return(
      <div style={st2}>
        {temp.map(elem=>elem)}
      </div>
    )
  }
}

ReactDOM.render(<App/>,document.getElementById('root'));

