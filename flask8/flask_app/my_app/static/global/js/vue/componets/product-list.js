Vue.component('product-list',{
    data:function(){
        return{
            products: [],
            productSelected:undefined,
            productIndexSelected:0,
            timeDelete:0,
            timeSave:0
        }
    },
    mounted(){
        this.findAll();
    },
    methods:{
        findAll: function(){
            console.log("hola mundo")

            fetch('http://127.0.0.1:5000/api/products/').then(
                res => res.json()
            ).then(
                res => this.products=res
            )
        },
        productDelete: function(product, index){
            this.timeDelete = new Date().getTime()
            this.productSelected = product
            this.productIndexSelected = index
        },
        productSave: function(){
            this.timeSave = new Date().getTime()
            this.productSelected = undefined
        },
        productUpdate: function(product, index){
            this.timeSave = new Date().getTime()
            this.productSelected = product
            this.productIndexSelected = index
        },
        eventProductDelete: function(){
            //console.log("Eliminado")
            this.$delete(this.products.data,this.productIndexSelected)
        },
        eventProductInsert: function(product){
            //console.log(product.data)
            this.products.data.push(product.data)
        },
        eventProductUpdate: function(product){
            this.products.data[this.productIndexSelected].name = product.data.name
            this.products.data[this.productIndexSelected].category_id = product.data.category_id
            this.products.data[this.productIndexSelected].category = product.data.category
            this.products.data[this.productIndexSelected].price = product.data.price
            //console.log(product.data.name)
        }
    },
    template:
    `
    <div class="mt-2">
        <button class="btn btn-outline-success" v-on:click="productSave">Crear</button>
        <div v-if="products.length == 0">
            <h1>No hay productos</h1>
            
        </div>
        <div v-else>
            <h1>Productos</h1>
        </div>
        <div class="jumbotron p-2 m-2 mt-2" v-for="(product,index) in products.data" >
            <h3>
                <a href="#">{{product.name}} </a>
            </h3>
            <h5>{{product.category}}</h5>

            <a v-on:click="productUpdate(product,index)" data-toggle="tooltip" data-placement="top" :title="'Actualizar producto ' + product.name" class="btn btn-outline-success btn-sm" href="#"><i class="fa fa-edit"></i> </a>

            <button v-on:click="productDelete(product,index)" data-placement="top" :title="'Eliminar producto' + product.name" :data-name="product.name" :data-id="product.id"  class="btn btn-outline-danger btn-sm" href="#"><i data-toggle="tooltip"  class="fa fa-trash"></i> </button>
        </div>
        <product-delete v-on:eventProductDelete="eventProductDelete" :time="timeDelete" :product="productSelected" ></product-delete>
        <product-save v-on:eventProductUpdate="eventProductUpdate" :productEdit="productSelected" v-on:eventProductInsert="eventProductInsert" :time="timeSave" ></product-save>
    </div>
    `
    
    
});