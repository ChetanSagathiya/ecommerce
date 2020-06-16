$('.add-to-cart').click(function(){
	var productId = this.dataset.product
	var action = this.dataset.action
	console.log('productId:', productId)
	$.ajax(
	{
		type:"GET",
		url: "/add_to_cart",
		data:{
			productId: productId,
			action: action,
			},
			success: function(data){
				var qty = parseInt($('sup').text())
				$('sup').val(qty+1)
				console.log("this is done here",qty)
			}
	})
})

$('.decrease-item').click(function(){
	var productId = this.dataset.product
	var action = this.dataset.action
	console.log("item decresed", productId, action)
	var qty = $('.qty').val();
	console.log("qty is ",qty)
	$.ajax(
	{
		type:"GET",
		url: "/add_to_cart",
		data:{
			productId: productId,
			action: action,
			},
			success: function(data){
				console.log("this is done here", qty)
					location.reload()
			}
	})
})

$('.increase-item').click(function(){
	var productId = this.dataset.product
	var action = this.dataset.action
	console.log("item decresed", productId, action)
	var qty = $('.qty').val();
	console.log("qty is ",qty)
	$.ajax(
	{
		type:"GET",
		url: "/add_to_cart",
		data:{
			productId: productId,
			action: action,
			},
			success: function(data){
				location.reload()
			}
	})
})