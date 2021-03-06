Vue.component('product-delete',{
    props:['product','time'],
    data:function(){
        return{
            products: []
        }
    },
    methods:{
        productDelete: function(){
            fetch('http://127.0.0.1:5000/api/products/' + this.product.id,{
                method:'DELETE'
            }).then(
                res => res.json()
            ).then(
                res => this.$emit("eventProductDelete")
            )
        }
    },
    watch:{
        time: function(newValue,oldValue){
            console.log(this.time + " " + this.product.name)
            $("#deleteModal").modal("show")
            //console.log(newValue + " " + oldValue)
        }
    },
    template:
    `
    <div  class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
        <div v-if="product" class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Borrar: <span>{{ product.name }}</span></h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            </div>
            <div class="modal-body">
            ¿Seguro que desea borrar el registro seccionado?
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
            <button v-on:click="productDelete" type="button" class="btn btn-danger" data-dismiss="modal">Borrar</button>
            </div>
        </div>
        </div>
    </div>
    `
    
    
});