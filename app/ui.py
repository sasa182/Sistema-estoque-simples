import tkinter as tk
from controller import add_product, list_products, search_product, remove_product, record_product, update_view, update_price, DB_PATH, HISTORY_DB_PATH
import tkinter.ttk as ttk


''' --------------------------------------------------------------------------------------------------------
'''

# ? quando o botão foi clicado sua respectiva função vai ser ativida que ent chamara a função de controller.py

def add_product_gui(name_entry, quantity_entry, price_entry):
    name = name_entry.get()
    quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    add_product(name, quantity, price)
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def show_products():
    product_window = tk.Toplevel()
    product_window.title("Lista de Produtos")
    
    products = list_products()

    tk.Label(product_window, text="ID").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(product_window, text="Nome").grid(row=0, column=1, padx=10, pady=10)
    tk.Label(product_window, text="Quantidade").grid(row=0, column=2, padx=10, pady=10)
    tk.Label(product_window, text="Preço (R$)").grid(row=0, column=3, padx=10, pady=10)

    for i, product in enumerate(products, start=1):
        tk.Label(product_window, text=product[0]).grid(row=i, column=0, padx=10, pady=5)
        tk.Label(product_window, text=product[1]).grid(row=i, column=1, padx=10, pady=5)
        tk.Label(product_window, text=product[2]).grid(row=i, column=2, padx=10, pady=5)
        tk.Label(product_window, text=product[3]).grid(row=i, column=3, padx=10, pady=5)

def search_product_gui(search_entry):
    search_term = search_entry.get()
    results = search_product(search_term)
    search_entry.delete(0, tk.END)
    
    search_window = tk.Toplevel()
    search_window.title("Resultados da Busca")

    tk.Label(search_window, text="ID").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(search_window, text="Nome").grid(row=0, column=1, padx=10, pady=10)
    tk.Label(search_window, text="Quantidade").grid(row=0, column=2, padx=10, pady=10)
    tk.Label(search_window, text="Preço (R$)").grid(row=0, column=3, padx=10, pady=10)

    for i, product in enumerate(results, start=1):
        tk.Label(search_window, text=product[0]).grid(row=i, column=0, padx=10, pady=5)
        tk.Label(search_window, text=product[1]).grid(row=i, column=1, padx=10, pady=5)
        tk.Label(search_window, text=product[2]).grid(row=i, column=2, padx=10, pady=5)
        tk.Label(search_window, text=product[3]).grid(row=i, column=3, padx=10, pady=5)

def remove_product_gui(remove_entry):
    product_id = remove_entry.get()
    remove_product(product_id)
    remove_entry.delete(0, tk.END)

def record_product_gui(record_entry, sale_quantity_entry):
    product_id = record_entry.get()
    sale_quantity = int(sale_quantity_entry.get())
    record_product(product_id, sale_quantity)
    record_entry.delete(0, tk.END)
    sale_quantity_entry.delete(0, tk.END)

def update_price_gui(product_id_entry, new_price_entry):
    product_id = product_id_entry.get()
    new_price = float(new_price_entry.get())
    update_price(product_id, new_price)
    product_id_entry.delete(0, tk.END)
    new_price_entry.delete(0, tk.END)


''' ---------------------------------------------------------------------------------------------------------
'''

# ? Janelas que aparecerão na tela

# janela principal
def main_window():
    window = tk.Tk()
    window.title("Sistema de Estoque")
    window.geometry("400x735+710+15")

    # Seção para adicionar produto
    tk.Label(window, text="Adicionar Produto", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(window, text="Nome do Produto:", width=20).grid(row=1, column=0, pady=5, sticky="e")
    name_entry = tk.Entry(window, width=30)
    name_entry.grid(row=1, column=1, pady=5)

    tk.Label(window, text="Quantidade:", width=20).grid(row=2, column=0, pady=5, sticky="e")
    quantity_entry = tk.Entry(window, width=20)
    quantity_entry.grid(row=2, column=1, pady=5)

    tk.Label(window, text="Preço (R$):", width=20).grid(row=3, column=0, pady=5, sticky="e")
    price_entry = tk.Entry(window, width=20)
    price_entry.grid(row=3, column=1, pady=5)

    tk.Button(window, text="Adicionar Produto", command=lambda: add_product_gui(name_entry, 
                                quantity_entry, price_entry)).grid(row=4, column=0, columnspan=2, pady=10)

    # Separador
    tk.Label(window, text="""-------------------------------------------------------------------------
    """).grid(row=5, column=0, columnspan=2, padx=10)

    # Seção para buscar produto
    tk.Label(window, text="Buscar Produto", font=("Arial", 14)).grid(row=6, column=0, columnspan=2, pady=0)

    tk.Label(window, text="Nome ou ID:", width=20).grid(row=7, column=0, pady=5, sticky="e")
    search_entry = tk.Entry(window, width=20)
    search_entry.grid(row=7, column=1, pady=5)

    tk.Button(window, text="Buscar", command=lambda: search_product_gui(search_entry)).grid(row=8, 
                                                                column=0, columnspan=2, pady=10)

    # Separador
    tk.Label(window, text="""-------------------------------------------------------------------------
    """).grid(row=9, column=0, columnspan=2, padx=10)

    # Seção para remover produto
    tk.Label(window, text="Remover Produto", font=("Arial", 14)).grid(row=10, column=0, columnspan=2, pady=10)

    tk.Label(window, text="ID do Produto:", width=20).grid(row=11, column=0, pady=5, sticky="e")
    remove_entry = tk.Entry(window, width=20)
    remove_entry.grid(row=11, column=1, pady=5)

    tk.Button(window, text="Remover Produto", command=lambda: remove_product_gui(remove_entry)).grid(row=12, 
                                                                    column=0, columnspan=2, pady=10)

    # Separador
    tk.Label(window, text="""-------------------------------------------------------------------------
    """).grid(row=13, column=0, columnspan=2, padx=10)

    # Seção para dar baixa no produto
    tk.Label(window, text="Baixa no Produto", font=("Arial", 14)).grid(row=14, column=0, columnspan=2, pady=10)

    tk.Label(window, text="ID do Produto:", width=20).grid(row=15, column=0, pady=5, sticky="e")
    record_entry = tk.Entry(window, width=20)
    record_entry.grid(row=15, column=1, pady=5)

    tk.Label(window, text="Quantidade do Produto:", width=20).grid(row=16, column=0, pady=5, sticky="e")
    sale_quantity_entry = tk.Entry(window, width=20)
    sale_quantity_entry.grid(row=16, column=1, pady=5)

    tk.Button(window, text="Dar Baixa", command=lambda: record_product_gui(record_entry, sale_quantity_entry)).grid(row=17, 
                                                                    column=0, columnspan=2, pady=10)

    # Separador
    # tk.Label(window, text="""-------------------------------------------------------------------------
    # """).grid(row=17, column=0, columnspan=2, padx=10)

    # # Botão para mostrar todos os produtos
    # tk.Button(window, text="Mostrar Todos os Produtos", command=show_products).grid(row=18, column=0, 
    #                                                                             columnspan=2)

    return window


# janela secundaria (não cabia na outra quis fazer isso)
def secondary_window():
    window = tk.Toplevel()
    window.title("2nd window")
    window.geometry("260x170+1130+300")

    def on_close():
        window.destroy() 
        
    window.protocol("WM_DELETE_WINDOW", on_close)
                                                                      
    tk.Label(window, text='Atualizar Preço', font=('Arial', 14)).grid(row=0, column=0, 
                                                            columnspan=2, padx=5, pady=10, sticky='e')
    tk.Label(window, text='ID do Produto', width=20).grid(row=1, column=0, 
                                                         padx=5, pady=5, sticky='e')
    
    tk.Label(window, text='Novo Preço (R$)', width=20).grid(row=2, column=0, 
                                                         padx=5, pady=5, sticky='e')
    product_id_entry = tk.Entry(window, width=10)
    product_id_entry.grid(row=1, column=1, pady=5)
    new_price_entry = tk.Entry(window, width=10)
    new_price_entry.grid(row=2, column=1, pady=5)

    tk.Button(window, text='SUMBMIT', command=lambda: update_price_gui(product_id_entry, 
                                                new_price_entry)).grid(row=3, column=0, columnspan=2, 
                                                                    padx=5, pady=5, sticky='e')
    return window


''' --------------------------------------------------------------------------------------------------------
'''

# ? TREE VIEWS (janelas tb)

# janela em tempo real da base de dados
def database_view_window():
    window = tk.Toplevel()
    window.title("Visão da Base de Dados")
    window.geometry("640x400+50+350")

    def on_close():
        window.destroy() 
        
    window.protocol("WM_DELETE_WINDOW", on_close)

    columns = ("ID", "Nome", "Quantidade", "Preço")
    columns_size = {
        "ID": 120,
        "Nome": 250,
        "Quantidade": 150,
        "Preço": 120
    }
    tree = ttk.Treeview(window, columns=columns, show='headings')

    for col in columns:
        size = columns_size.get(col)
        tree.heading(col, text=col)
        tree.column(col, width=size, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)
    update_view(tree, db_path=DB_PATH, table_name='products')


# janela em tempo real do registro de ações
def logs_view_window():
    window = tk.Toplevel()
    window.title("Visão do Registro do Sistema")
    window.geometry("640x290+50+15")

    def on_close():
        window.destroy() 
        
    window.protocol("WM_DELETE_WINDOW", on_close)

    columns = ("ID", "OPERAÇÃO", "DATA", "QUANTIDADE", "PREÇO ANTIGO", "PREÇO")
    columns_size = {
        "ID": 70,
        "OPERAÇÃO": 110,
        "DATA": 160,
        "QUANTIDADE": 100,
        "PREÇO ANTIGO": 100,
        "PREÇO": 100
    }
    tree = ttk.Treeview(window, columns=columns, show='headings')

    for col in columns:
        size = columns_size.get(col)
        tree.heading(col, text=col)
        tree.column(col, width=size, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)
    update_view(tree, db_path=HISTORY_DB_PATH, table_name='products_history')
    

''' --------------------------------------------------------------------------------------------------------
'''


if __name__ == "__main__":
    root = main_window()
    database_view_window()
    logs_view_window()
    secondary_window()
    root.mainloop()

    # dessa forma faz com que elas aparecam de forma simultanea e todas permanecam responsivas (n sei como)
    # o main loop ta na principal, se ela for fechada as outras fecham, mas não o contrario