Search.setIndex({docnames:["about","index","modules","roco","roco.api","roco.api.utils","roco.builders","roco.derived","roco.derived.components","roco.derived.composables","roco.derived.composables.fegraph","roco.derived.ports","roco.derived.utils","roco.library","roco.tests","roco.utils","tutorial"],envversion:50,filenames:["about.rst","index.rst","modules.rst","roco.rst","roco.api.rst","roco.api.utils.rst","roco.builders.rst","roco.derived.rst","roco.derived.components.rst","roco.derived.composables.rst","roco.derived.composables.fegraph.rst","roco.derived.ports.rst","roco.derived.utils.rst","roco.library.rst","roco.tests.rst","roco.utils.rst","tutorial.rst"],objects:{"roco.api":{"interface":[4,0,0,"-"],component:[4,0,0,"-"],composable:[4,0,0,"-"],connection:[4,0,0,"-"],parameterized:[4,0,0,"-"],port:[4,0,0,"-"],utils:[5,0,0,"-"]},"roco.api.component":{Component:[4,1,1,""],get_subcomponent_object:[4,3,1,""]},"roco.api.component.Component":{add_connection:[4,2,1,""],add_interface:[4,2,1,""],add_subcomponent:[4,2,1,""],append:[4,2,1,""],assemble:[4,2,1,""],attach:[4,2,1,""],define:[4,2,1,""],del_interface:[4,2,1,""],del_subcomponent:[4,2,1,""],eval_connections:[4,2,1,""],eval_constraints:[4,2,1,""],eval_interfaces:[4,2,1,""],eval_subcomponents:[4,2,1,""],get_interface:[4,2,1,""],get_subcomponent:[4,2,1,""],get_subcomponent_interface:[4,2,1,""],inherit_all_interfaces:[4,2,1,""],inherit_constraints:[4,2,1,""],inherit_interface:[4,2,1,""],make:[4,2,1,""],make_component_hierarchy:[4,2,1,""],make_component_tree:[4,2,1,""],make_output:[4,2,1,""],recurse_component_tree:[4,2,1,""],reset:[4,2,1,""],resolve_subcomponent:[4,2,1,""],resolve_subcomponents:[4,2,1,""],set_interface:[4,2,1,""],set_subcomponent_parameter:[4,2,1,""],to_yaml:[4,2,1,""]},"roco.api.composable":{Composable:[4,1,1,""]},"roco.api.composable.Composable":{"new":[4,2,1,""],add_component:[4,2,1,""],add_interface:[4,2,1,""],append:[4,2,1,""],attach:[4,2,1,""],make_output:[4,2,1,""]},"roco.api.connection":{Connection:[4,1,1,""]},"roco.api.connection.Connection":{get_name:[4,2,1,""],get_port_matchings:[4,2,1,""]},"roco.api.interface":{Interface:[4,1,1,""]},"roco.api.interface.Interface":{get_name:[4,2,1,""],get_ports:[4,2,1,""]},"roco.api.parameterized":{Parameterized:[4,1,1,""]},"roco.api.parameterized.Parameterized":{add_constraint:[4,2,1,""],add_parameter:[4,2,1,""],all_parameters:[4,2,1,""],check_constraints:[4,2,1,""],del_constraint:[4,2,1,""],del_parameter:[4,2,1,""],extend_constraints:[4,2,1,""],get_constraints:[4,2,1,""],get_name:[4,2,1,""],get_parameter:[4,2,1,""],inherit_parameters:[4,2,1,""],set_name:[4,2,1,""],set_parameter:[4,2,1,""],solve:[4,2,1,""]},"roco.api.port":{Port:[4,1,1,""]},"roco.api.port.Port":{add_allowable_mate:[4,2,1,""],add_recommended_mate:[4,2,1,""],can_mate:[4,2,1,""],constrain:[4,2,1,""],get_compatible_ports:[4,2,1,""],get_parent:[4,2,1,""],get_value:[4,2,1,""],prefix:[4,2,1,""],set_driven_value:[4,2,1,""],set_input_value:[4,2,1,""],set_output_value:[4,2,1,""],set_parent:[4,2,1,""],should_mate:[4,2,1,""],to_string:[4,2,1,""],update:[4,2,1,""]},"roco.api.utils":{variable:[5,0,0,"-"]},"roco.api.utils.variable":{Variable:[5,1,1,""],eval_equation:[5,3,1,""]},"roco.api.utils.variable.Variable":{default_assumptions:[5,4,1,""],get_default_value:[5,2,1,""],get_name:[5,2,1,""],get_solved_value:[5,2,1,""],get_value:[5,2,1,""],set_default_value:[5,2,1,""],set_name:[5,2,1,""],set_solved_value:[5,2,1,""]},"roco.derived":{components:[8,0,0,"-"],composables:[9,0,0,"-"],ports:[11,0,0,"-"],utils:[12,0,0,"-"]},"roco.derived.components":{folded_component:[8,0,0,"-"],mechanical_component:[8,0,0,"-"]},"roco.derived.components.folded_component":{FoldedComponent:[8,1,1,""]},"roco.derived.components.folded_component.FoldedComponent":{define:[8,2,1,""]},"roco.derived.components.mechanical_component":{MechanicalComponent:[8,1,1,""]},"roco.derived.components.mechanical_component.MechanicalComponent":{define:[8,2,1,""]},"roco.derived.composables":{fegraph:[10,0,0,"-"],graph_composable:[9,0,0,"-"],virtual_composable:[9,0,0,"-"]},"roco.derived.composables.fegraph":{face:[10,0,0,"-"],face_edge_graph:[10,0,0,"-"],hyper_edge:[10,0,0,"-"]},"roco.derived.composables.fegraph.face":{Face:[10,1,1,""],Rectangle:[10,1,1,""],RegularNGon2:[10,1,1,""],RegularNGon:[10,1,1,""],RightTriangle:[10,1,1,""],Square:[10,1,1,""],Triangle:[10,1,1,""]},"roco.derived.composables.fegraph.face_edge_graph":{FaceEdgeGraph:[10,1,1,""],dxf_write:[10,3,1,""],inflate:[10,3,1,""],stl_write:[10,3,1,""]},"roco.derived.composables.fegraph.face_edge_graph.FaceEdgeGraph":{add_face:[10,2,1,""],add_tab:[10,2,1,""],attach_face:[10,2,1,""],del_face:[10,2,1,""],dotransform:[10,2,1,""],flip:[10,2,1,""],get_3d_com:[10,2,1,""],get_edge:[10,2,1,""],get_face:[10,2,1,""],graph_obj:[10,2,1,""],invert_edges:[10,2,1,""],merge_edge:[10,2,1,""],mirror_x:[10,2,1,""],mirror_y:[10,2,1,""],place:[10,2,1,""],prefix:[10,2,1,""],print_graph:[10,2,1,""],rebuild_edges:[10,2,1,""],rename_edge:[10,2,1,""],show_graph:[10,2,1,""],split_edge:[10,2,1,""],tabify:[10,2,1,""],to_dxf:[10,2,1,""],to_stl:[10,2,1,""],to_svg:[10,2,1,""],transform:[10,2,1,""],unplace:[10,2,1,""]},"roco.derived.composables.fegraph.hyper_edge":{HyperEdge:[10,1,1,""]},"roco.derived.composables.graph_composable":{Decoration:[9,1,1,""],GraphComposable:[9,1,1,""]},"roco.derived.composables.graph_composable.Decoration":{append:[9,2,1,""],attach:[9,2,1,""],make_output:[9,2,1,""]},"roco.derived.composables.graph_composable.GraphComposable":{append:[9,2,1,""],attach:[9,2,1,""],make_output:[9,2,1,""],split_merged_edges:[9,2,1,""]},"roco.derived.composables.virtual_composable":{VirtualComposable:[9,1,1,""]},"roco.derived.composables.virtual_composable.VirtualComposable":{getContainer:[9,2,1,""],makeOutput:[9,2,1,""],setContainer:[9,2,1,""]},"roco.derived.ports":{code_port:[11,0,0,"-"],edge_port:[11,0,0,"-"],face_port:[11,0,0,"-"],six_dof_port:[11,0,0,"-"]},"roco.derived.ports.code_port":{CodePort:[11,1,1,""]},"roco.derived.ports.code_port.CodePort":{can_mate:[11,2,1,""],constrain:[11,2,1,""],get_label:[11,2,1,""],mangle:[11,2,1,""]},"roco.derived.ports.edge_port":{EdgePort:[11,1,1,""]},"roco.derived.ports.edge_port.EdgePort":{constrain:[11,2,1,""],get_edges:[11,2,1,""],get_points:[11,2,1,""],prefix:[11,2,1,""],update:[11,2,1,""]},"roco.derived.ports.face_port":{FacePort:[11,1,1,""]},"roco.derived.ports.face_port.FacePort":{can_mate:[11,2,1,""],get_face_name:[11,2,1,""],get_points:[11,2,1,""]},"roco.derived.ports.six_dof_port":{SixDOFPort:[11,1,1,""]},"roco.derived.ports.six_dof_port.SixDOFPort":{get_points:[11,2,1,""]},"roco.tests":{test_composable:[14,0,0,"-"]},"roco.tests.test_composable":{TestComposable:[14,1,1,""]},"roco.tests.test_composable.TestComposable":{test_new:[14,2,1,""]},"roco.utils":{io:[15,0,0,"-"],mymath:[15,0,0,"-"],utils:[15,0,0,"-"]},"roco.utils.io":{load_yaml:[15,3,1,""]},"roco.utils.mymath":{D:[15,1,1,""],SetPackage:[15,1,1,""],cumsum:[15,3,1,""],deg2rad:[15,3,1,""],diag:[15,3,1,""],difference:[15,3,1,""],difference_exceeds:[15,3,1,""],dot:[15,3,1,""],norm:[15,3,1,""],rad2deg:[15,3,1,""],round:[15,3,1,""],rows:[15,3,1,""],sum:[15,3,1,""],use_numpy:[15,3,1,""],use_sympy:[15,3,1,""]},"roco.utils.mymath.D":{default_assumptions:[15,4,1,""]},"roco.utils.mymath.SetPackage":{use_numpy:[15,4,1,""]},"roco.utils.utils":{decorate_graph:[15,3,1,""],memoized:[15,1,1,""],prefix:[15,3,1,""],print_equations:[15,3,1,""],print_parameters:[15,3,1,""],print_summary:[15,3,1,""],scheme_list:[15,4,1,""],scheme_repr:[15,3,1,""],scheme_string:[15,3,1,""],try_import:[15,3,1,""]},roco:{__init__:[3,0,0,"-"],api:[4,0,0,"-"],builders:[6,0,0,"-"],derived:[7,0,0,"-"],library:[13,0,0,"-"],tests:[14,0,0,"-"],utils:[15,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function","4":"py:attribute"},terms:{"6dof":11,"abstract":4,"boolean":[4,11],"case":14,"class":[4,5,7,8,9,10,11,12,14,15],"default":[4,5,11],"enum":[],"final":[4,9],"float":10,"function":[4,5,8,9,10,12,15],"import":15,"int":[4,10],"new":[4,5,10],"return":[4,5,9,10,11,15],"true":[4,11],For:4,The:[3,4,5,6,7,8,9,10,11,12,13,14,15],Uses:[],With:9,about:4,accord:10,achiev:1,act:[4,8],add:[4,8,9,10,11,15],add_allowable_m:4,add_compon:4,add_connect:4,add_constraint:4,add_fac:10,add_interfac:4,add_paramet:4,add_parameter_constraint:[],add_recommended_m:4,add_subcompon:4,add_tab:10,addcompon:[],added:[4,11],addit:9,adjac:10,aid:[],all:[4,8,9,10],all_paramet:4,allow:[3,4,8,9,10],allow_overlap:[],allparamet:4,alreadi:4,also:[4,8],ambigu:4,analog_port:[3,7],angl:[8,10],ani:[4,9],anonym:4,anoth:4,apart:10,api:[2,3,5,7,8,9,11],append:[4,9],append_draw:[],appli:[],appliedundef:15,arbitrari:[4,8],area:10,arg:[4,5,8,9,10,11,15],argument:[4,8,9,15],around:[],arrai:4,assembl:4,assign:[],associ:[4,10,11],attach:[4,9,10],attach_fac:10,attempt:[4,15],attribut:[4,9,10,11,15],attributeerror:11,autodoc:[],automat:4,avail:4,avoid:4,axes:15,axi:15,base:[4,5,7,8,9,10,11,14,15],been:[4,5,9],befor:4,being:[4,9,10],belong:4,bend:10,better:[4,11],between:[4,10],bool:[4,8,10],both:4,bound:[],boundari:10,box:[],build:6,builder:[2,3],built:8,cach:15,cad:[],calcul:10,call:[4,15],can:[4,6,8,9,11,13,15],can_mat:[4,11],cannot:4,caus:[],center:10,certain:6,chang:[4,10],charact:4,check:[4,11],check_constraint:4,cleanup:4,clockwis:[],code:[4,11,14],code_compon:[3,7],code_compos:[3,7],code_port:[3,7],codecompos:[],codeport:11,collect:[4,10],com2d:10,com4d:10,combin:4,come:4,commonli:10,compar:[4,11],compat:[4,11],compil:[1,3],compon:[3,7,9,11,13,15],component_obj:4,componentobj:[],compos:[3,7,8,10],comput:[],conneciton:4,connect:[3,9,10,11],consecut:10,consist:10,constant:4,constrain:[4,11],constraint:[4,8,11],construct:[8,10],constructor:4,contain:[4,5,6,7,8,9,10,11,12,13,14,15],containercompos:9,content:1,conveni:10,convent:[],convert:[9,10,15],coord:[],coordin:10,copi:[],core:[4,5,15],correctli:[],correspond:4,counter:[],creat:[4,9,10,13],creation:4,cross:10,cumsum:15,current:[4,5],custom:4,cut:10,data:[4,10,11],decor:[9,10,15],decorate_graph:15,default_assumpt:[5,15],defin:[4,8,10],definit:[4,10],deg2rad:15,deg:[],del_constraint:4,del_fac:10,del_interfac:4,del_paramet:4,del_subcompon:4,delet:[4,10],delimit:15,denot:[4,11],depend:[9,12],depict:4,deprec:[],deriv:[2,3,4,8,9,10,11,12],design:[3,4,6,9],desir:[],devic:4,dfajioj:10,diag:15,dict:[4,8,9,10],dictat:4,dictionari:[4,10],differ:[4,15],difference_exce:15,differenti:10,digital_port:[3,7],dimens:[],dimenst:[],direct:10,direction:[],directori:[4,9],displai:[3,10],doe:[4,11],dot:[4,15],dotransform:10,doubl:10,double_port:[3,7],down:4,draw:[3,7,9],drawing_edg:[3,7,9],drawingedg:[],drawn:9,driven:4,dtype:11,dummi:[4,5],dxf:10,dxf_write:10,each:[4,10,15],edg:[9,10,11],edge1:10,edge2:10,edge_from:[],edge_from_pt:[],edge_nam:11,edge_port:[3,7],edge_typ:10,edgenam:[],edgeport:11,edgetyp:10,either:[4,10],electrical_compon:[3,7],electrical_compos:[3,7],electrical_port:[3,7],element:4,elist:15,elong:[],els:4,empti:4,encapsul:4,endpoint:[],enforc:4,engin:[],equal:[4,11],equat:5,error:9,euler:8,eval_connect:4,eval_constraint:4,eval_equ:5,eval_interfac:4,eval_subcompon:4,evalu:[4,5],even:[],exampl:4,except:9,exist:4,expr:15,express:[4,5,15],extend:4,extend_constraint:4,face:[3,7,8,9,11,15],face_angl:10,face_edg:10,face_edge_graph:[3,7,9],face_flip:10,face_port:[3,7],faceedgegraph:[9,10],facenam:10,faceport:11,factor:[],fals:[4,8,10,11,15],fegraph:[3,7,9],file:[4,9,10],file_dir:[4,9],file_nam:[4,15],filedir:9,filenam:[4,10],find:10,first:[9,10],flip:10,float64:[],float_port:[3,7],fold:[8,10],foldabl:8,folded_compon:[3,7],foldedcompon:[8,9],follow:11,forc:10,force_const:[],force_liter:4,form:[],format:[],found:10,from:[4,7,8,9,10,11,15],from_edg:10,from_graph:[],from_interfac:[4,9],from_nam:4,from_port:4,fromnam:10,fromport:[],func:15,gener:[4,9],geometr:[],geometri:10,get:[1,4,9,11],get_3d_com:10,get_all_default:[],get_all_sub:[],get_compatible_port:4,get_constraint:4,get_default:[],get_default_valu:5,get_dimens:[],get_edg:[10,11],get_fac:10,get_face_nam:11,get_interfac:4,get_label:11,get_nam:[4,5],get_par:4,get_paramet:4,get_point:11,get_port:4,get_port_match:4,get_solved_valu:5,get_subcompon:4,get_subcomponent_interfac:4,get_subcomponent_object:4,get_valu:[4,5],get_variable_sub:[],get_variable_valu:[],getcontain:9,give:4,given:[4,5,9,10,11,15],goal:1,goe:4,graph:[4,8,9,10,11],graph_compos:[3,7],graph_obj:10,graphcompos:[9,10],hand:10,handl:4,has:[4,5,9,11],have:[4,8,9,11],helper:[4,5,10,12,15],hierarch:4,hierarchi:4,high:3,hold:[4,11],homogen:10,how:[],hyper_edg:[3,7,9],hyperedg:[10,11],ident:[],identifi:4,ignor:4,imag:4,implement:[4,11],impos:4,in_port:[3,7],includ:4,index:1,indoubleport:11,inflat:10,infloatport:11,inform:4,inherit:[4,11],inherit_all_interfac:4,inherit_constraint:4,inherit_interfac:4,inherit_paramet:4,inintport:11,inport:11,input:4,insid:4,instanc:4,instanti:4,instringport:11,int_port:[3,7],integ:4,interfac:[3,9],interface1:4,interface2:4,intern:4,interpret:15,invalid:4,invert:10,invert_edg:10,is_input:4,is_liter:4,is_output:4,is_symbol:[],iter:[10,15],its:10,itself:4,join:10,joint:10,kei:4,keyerror:4,keyword:[4,8],kwarg:[4,8,9,11],label:11,later:15,layer:8,learn:1,left:4,length:[10,11],lesson:1,level:[3,4],librari:[2,3],list:[4,10,11,15],liter:[],load:[4,13],load_yaml:15,locat:[8,15],made:4,mai:[4,9],make:[4,9,10],make_component_hierarchi:4,make_component_tre:4,make_output:[4,9],makeoutput:9,mangl:11,mass:10,match:[4,11],mate:[4,11],mate_typ:4,matrix:10,maximum:[],meant:[4,9,10],mechan:8,mechanical_compon:[3,7],mechanicalcompon:8,member:[4,9],memoiz:15,mere:4,merg:[9,10],merge_edg:10,meta:[],method:[4,11],methodnam:14,midpoint:[],midpt:[],mirror_i:10,mirror_x:10,mirrori:[],mirrorx:[],mode:15,modifi:[4,10],modul:[1,3,7],more:[4,10,11],mountain:[],multipl:15,must:9,my_nam:4,my_nod:4,mymath:3,name:[4,5,10,11,15],nearest:[],necessari:[4,9,10],new_compos:[4,9],new_edg:10,new_fac:10,new_interfac:4,new_nam:[],new_par:4,new_prefix:[4,9],newcompos:[],newli:4,newprefix:[],ngon:10,node:4,non:[],none:[4,5,8,9,10,11,15],nontang:9,norm:15,notat:15,number:4,numer:10,numpi:[],obj:11,object:[4,7,8,9,10,11,15],object_typ:4,offset:15,offset_di:15,offset_dx:15,old:4,old_nam:[],one:[4,9],ones:4,onli:[],option:4,order:[4,10],ordereddict:4,origin:[8,10],other:4,other_port:[4,11],otherwai:[],otherwis:[4,5,11],out:[],out_port:[3,7],outdoubleport:11,outfloatport:11,outintport:11,outport:11,output:[4,9,13],outstringport:11,overal:4,overlap:[],overrid:[4,11],overridden:4,overwritten:[],packag:[1,2],page:1,pair:[4,15],param:4,paramet:[4,5,8,11,15],parameter:3,parameter_nam:[],parent:[4,11],part:10,pass:4,perform:4,physic:[4,8,11],place:[4,9,10],place_fac:[],plane:10,point:[4,10,11],polygon:10,port1:9,port2:9,port:[3,7,9],posit:[8,10],prebuilt:13,prefix2:9,prefix:[4,9,10,11,15],prepend:[],previou:[],previous:[],primit:15,print:[10,15],print_equ:15,print_graph:10,print_paramet:15,print_summari:15,process:9,produc:[4,9],project:1,provid:[4,10],pt1:[],pt2:[],pts1:15,pts2:15,pts2d:10,pts3d:10,pts4d:10,pwm_port:[3,7],pydot:4,python:4,quadrilater:10,quat:8,quaternion:8,rad2deg:15,rad:[],radian:[],radiu:10,rais:[4,5,9,11],rebuild:10,rebuild_edg:10,recommend:4,rectangl:10,recurs:4,recurse_component_tre:4,redefin:[4,9],reevalu:15,refer:[4,9,10],regular:10,regularngon2:10,regularngon:10,rel:[],relat:[4,8,15],relationship:4,remov:[4,10],removetarget:[],renam:10,rename_edg:10,replac:4,repres:[4,8,9,10,11,15],represent:[4,10],requir:[5,12,15],reset:4,resolve_subcompon:4,retriev:4,right:10,righttriangl:10,robot:[1,3,4,9],roco:[4,5,6,8,9,10,11,13,14,15],root:4,rotat:[8,15],round:15,row:15,rule:[4,10],run:6,runtest:14,same:[4,11,15],satisfi:[4,11],save_to_fil:[],scale:10,scheme:15,scheme_list:15,scheme_repr:15,scheme_str:15,scope:[],script:6,search:1,second:[9,10],self:5,semant:[4,11],separ:4,set:[4,5,9,10,11],set_default_valu:5,set_driven_valu:4,set_input_valu:4,set_interfac:4,set_nam:[4,5],set_output_valu:4,set_par:4,set_paramet:4,set_solved_valu:5,set_subcomponent_paramet:4,set_variable_solv:[],setcontain:9,setpackag:15,sever:10,should:[4,9,10],should_mat:4,show_graph:10,side:10,singl:4,six_dof_port:[3,7],sixdofport:11,slot:10,slot_decor:10,slot_fac:10,smaller:[],soft:4,solv:[4,5,8],some:[4,15],space:[8,10],special:7,specif:[4,11,15],specifi:4,split:[9,10],split_edg:10,split_merged_edg:9,squar:10,start:[1,8],state:[4,8],stl:10,stl_write:10,store:[4,8],str:[4,9,10,11,15],string:[4,9,10,11,15],string_port:[3,7],structur:8,sub:4,subclass:10,subcompon:4,subcopon:[],subnam:4,subpackag:[1,2],subparamet:[],substitut:[],sum:15,summari:[1,15],support:[],surfac:10,svg:10,swap:[],symbol:[4,5],symmetr:[],sympi:[4,5,15],tab:[3,7,10],tab_decor:10,tab_fac:10,tab_width:10,tabifi:10,tabwidth:10,take:4,taken:[],target:[],tell:4,test:[2,3],test_add_parameter_keyerror:[],test_add_parameter_return:[],test_check_constraint:[],test_compos:3,test_del_paramet:[],test_dummi:[],test_new:14,test_parameter:3,testcas:14,testcompos:14,testparameter:[],thei:9,them:4,thi:[1,4,6,8,9,10,11,13,14],thick:10,three:10,through:10,tie:4,tied:4,time:15,tkinter:9,to_dxf:10,to_interfac:[4,9],to_nam:4,to_port:[4,11],to_stl:10,to_str:4,to_svg:10,to_yaml:4,todraw:[],togeth:[4,9],token:[],tol:15,tonam:10,top:8,toport:[],transform2d:10,transform3d:10,transform:[9,10],transform_2d:[],transfrom3d:10,translat:10,treat:[],tree:4,tree_nam:4,triangl:10,try_import:15,tupl:[4,10,15],tutori:1,two:[4,9,10],type:[4,8,10,11],unfold:[],uniniti:4,uniqu:4,unit:14,unittest:14,unplac:10,updat:[4,11],upon:[4,9],usabl:[4,9],use:[8,9,10],use_numpi:15,use_sympi:15,used:[1,4,10],user:10,using:[5,8,9],util:[2,3,4,7],val:[],valid:[],vallei:[],valu:[4,5,15],valueerror:[4,5],variabl:[3,4],variou:5,verifi:4,version:[],vertex:10,vertex_coordin:[],vertic:10,violat:4,virtual:9,virtual_compos:[3,7],virtual_electrical_port:[3,7],virtualcompos:9,well:[4,9,10,11],what:4,when:[4,11],where:4,whether:[4,8,10,11,15],which:[4,8,9,11],whose:4,width:10,within:8,work:4,write:[4,10],wrt:[],xmax:[],xmin:[],yaml:4,yaml_fil:[4,8],ymax:[],ymin:[]},titles:["Project Summary","Welcome to roco&#8217;s documentation!","ROCO Modules","roco Package","api Package","utils Package","builders Package","derived Package","components Package","composables Package","fegraph Package","ports Package","utils Package","library Package","tests Package","utils Package","Roco Tutorial"],titleterms:{achiev:0,analog_port:11,api:[1,4],autodoc:[],builder:6,code_compon:8,code_compos:9,code_port:11,compon:[4,8],compos:[4,9],connect:4,deriv:7,digital_port:11,displai:15,document:1,double_port:11,draw:10,drawing_edg:10,edge_port:11,electrical_compon:8,electrical_compos:9,electrical_port:11,face:10,face_edge_graph:10,face_port:11,fegraph:10,float_port:11,folded_compon:8,get:16,goal:0,graph_compos:9,hyper_edg:10,in_port:11,indic:1,int_port:11,interfac:4,learn:0,lesson:0,librari:13,mechanical_compon:8,modul:[2,4,5,8,9,10,11,12,14,15],mymath:15,out_port:11,packag:[3,4,5,6,7,8,9,10,11,12,13,14,15],parameter:4,port:[4,11],project:0,pwm_port:11,roco:[1,2,3,16],six_dof_port:11,start:16,string_port:11,subpackag:[3,4,7,9],summari:0,tab:12,tabl:1,test:14,test_compos:14,test_parameter:14,tutori:16,util:[5,12,15],variabl:5,virtual_compos:9,virtual_electrical_port:11,welcom:1}})