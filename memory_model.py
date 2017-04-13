class Block:
	def __init__(self, content, allocated):
		self.content = content

		#For headers and footers of implicit linked lists
		self.allocated = allocated



class ImplicitList:
	def __init__(self):
		self.heap = [Block(0, False) for i in range(200)]
		self.heap[0].content = 200
		self.heap[199].content = 200

		#For fitting blocks
		self.location = 0

	def add_to_selected_location(self, location_start, word):
		#setting free spot's new footer
		self.heap[location_start +  self.heap[location_start].content-1].content = self.heap[location_start].content - len(word) - 2
		#setting free spot's new  header
		self.heap[location_start + len(word) + 2].content = self.heap[location_start].content - len(word) - 2


		#set header
		self.heap[location_start].allocated = True
		self.heap[location_start].content = len(word) + 2

		#set payload
		for i in range(len(word)):
			self.heap[location_start + 1 + i].content = word[i]

		#set footer
		self.heap[location_start+len(word) + 1].allocated = True
		self.heap[location_start+len(word) + 1].content = len(word) + 2


	def free(self, index_of_header):
		index_of_footer = self.heap[index_of_header].content + index_of_header - 1

		#Erase all content
		for i in range(index_of_footer-index_of_header-1):
			self.heap[index_of_header+i+1].content = 0

		self.heap[index_of_header].allocated = False
		self.heap[index_of_footer].allocated = False

		self.coalesce(index_of_header, index_of_footer)

	def coalesce(self, index_of_header, index_of_footer):
		size = self.heap[index_of_header].content

		#Previous blocks are free
		if index_of_header != 0 and self.heap[index_of_header-1].allocated is not True:
			size = self.heap[index_of_header-1].content + size

			#Set prev's header and current's footer to new size
			self.heap[index_of_footer].content = size
			self.heap[index_of_footer-self.heap[index_of_footer].content+1].content = size

			#Remove prev's footer and current's header
			self.heap[index_of_header].content = 0
			self.heap[index_of_header-1].content = 0

			index_of_header = index_of_footer-size+1

		
		#Following blocks are free
		if self.heap[index_of_footer+1].allocated is not True:
			size = self.heap[index_of_footer+1].content + size

			#Set following's footer and current header to new size
			self.heap[index_of_header+size-1].content = size
			self.heap[index_of_header].content = size

			
			#Remove current footer and following's header
			self.heap[index_of_footer].content = 0
			self.heap[index_of_footer+1].content = 0
			
		


	def add_using_first_fit(self, word):
		self.location = 0
		
		while self.heap[self.location].allocated is not False or self.heap[self.location].content < len(word) + 2:
			self.location += self.heap[self.location].content

		while self.location + len(word) + 2 > len(self.heap):
			self.reallocate(self.location)

		self.add_to_selected_location(self.location, word)


	def add_using_next_fit(self, word):
		while self.heap[self.location].allocated is not False or self.heap[self.location].content < len(word) + 2:
			self.location += self.heap[self.location].content

		while self.location + len(word) + 2 > len(self.heap):
			self.reallocate(self.location)

		self.add_to_selected_location(self.location, word)

	def add_using_best_fit(self, word):
		self.location = 0
		current_best_location = len(self.heap)
		current_best_difference = len(self.heap)

		while self.location < len(self.heap) and self.location + len(word) + 2 < len(self.heap):
			if self.heap[self.location].allocated is False:
				if self.heap[self.location].content > len(word) + 2 and self.heap[self.location].content - len(word) - 2  < current_best_difference:
					current_best_difference = self.heap[self.location].content - len(word) - 2
					current_best_location = self.location
			self.location += self.heap[self.location].content 
		

		while current_best_location + len(word) + 2 > len(self.heap):
			self.reallocate(self.location)

		self.add_to_selected_location(current_best_location, word)


	#Enlarges memory (analagous to sbrk())
	def reallocate(self, current_location):
		for each in range(200):
			self.heap.append(Block(0, False))

		self.heap[len(self.heap)-201].content = 0
		self.heap[current_location].content = len(self.heap) - current_location
		self.heap[len(self.heap)-1].content = self.heap[current_location].content



l = ImplicitList()

l.add_using_best_fit("blah blah blah")
l.add_using_best_fit("ah")
l.free(0)
l.add_using_best_fit("meh meh meh meh meh")
l.add_using_best_fit("hah aha")
l.reallocate(41)


for i in range(len(l.heap)):
	print l.heap[i].content